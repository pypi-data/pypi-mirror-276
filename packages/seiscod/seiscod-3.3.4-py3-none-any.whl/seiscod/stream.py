# built in
from typing import Union, List
import types
import warnings
from typing import Union
from copy import deepcopy
from multiprocessing import Pool, cpu_count

# official deps
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap

# this package
from tempoo.windows import split_time_into_windows
from seiscod.signal.pws import pws
from seiscod.signal.waveformclustering import \
    waveform_corr_coeff, waveform_distances, waveform_clustering
from seiscod.trace import Trace, FFTTrace
from seiscod.errors import EmptyStreamError, DataTypeError, \
    SamplingError, SamplingRateError, NptsError, StarttimeError
from seiscod.readwrite.npz.readnpz import NPZReader, write_npz
from seiscod.graphic import show_stream, shade_stream


class Stream(list):

    def __init__(self, traces: list = None):
        """
        initiate the instance with the stream (obspy or obsmax4)
        or nothing :  see self.from_obspy or self.from_npz"""

        if traces is None:
            super().__init__([])

        elif isinstance(traces, list) or isinstance(traces, Stream):
            for trace in traces:
                if not isinstance(trace, Trace):
                    raise TypeError(type(traces))
            super().__init__(traces)

        else:
            raise NotImplementedError(type(traces))

    def copy(self):
        return deepcopy(self)

    def __str__(self):
        return "\n".join([str(tr) for tr in self])

    def __repr__(self):
        return self.__str__()

    # ============ convertion from or to obspy
    def from_obspy(self, stream, **kwargs):
        """populate the objects with an obspy stream
        use it to convert obspy into a seiscod object
        kwargs passed to Trace.from_obspy
        """

        for obspy_trace in stream:
            trace = Trace()
            trace.from_obspy(obspy_trace, **kwargs)
            self.append(trace)

        return self

    def to_obspy(self):
        # warning this module must keep independant from obspy, I just assume here that the user is
        # trying to convert this object to obspy, so obspy is installed
        try:
            # I don't want anything from obspy in the top imports !!!
            # this may fuck up matplotlib behavior
            from obspy.core.stream import Stream as ObspyStream
        except ImportError as e:
            e.args = ('obspy not installed', )
            raise e

        obspy_traces = []
        for seiscod_trace in self:
            obspy_trace = seiscod_trace.to_obspy()
            obspy_traces.append(obspy_trace)

        return ObspyStream(obspy_traces)

    # ============
    def check_data_types(self):

        if not len(self):
            raise EmptyStreamError()

        dtype = self[0].data.dtype
        for trace in self[1:]:
            if dtype != trace.data.dtype:
                raise DataTypeError
        return dtype

    def check_stream_sampling_regularization(self):
        """
        verifies that all traces have the same time vector
        :return:
        """

        if not len(self):
            raise EmptyStreamError()

        msg = 'the stream is not regularized, please resample {}, ({}, {})'
        nptss = np.asarray([tr.npts for tr in self], int)
        deltas = np.asarray([tr.delta for tr in self], float)
        starttimes = np.asarray([tr.starttime for tr in self], float)

        npts = self[0].npts
        delta = self[0].delta
        starttime = self[0].starttime

        is_npts = nptss == npts
        is_delta = deltas == delta
        is_start = np.abs(starttimes - starttime) < 1.e-16

        if not is_npts.all():
            raise NptsError(msg.format("npts", npts, nptss[~is_npts][0]))

        elif not is_delta.all():
            raise SamplingRateError(msg.format("delta", delta, deltas[~is_delta][0]))

        elif not is_start.all():
            raise StarttimeError(msg.format("starttime", starttime, starttimes[~is_start][0]))

        return npts, delta, starttime

    def is_regularized(self):
        try:
            self.check_stream_sampling_regularization()
            ans = True
        except (NptsError, SamplingRateError, StarttimeError) as err:
            # other exceptions will crash
            ans = False
        return ans

    def regularize(self, fill_value: float = 0.0, qc: bool = True):
        """
        uniformize the sampling rate for all traces in the stream
        if the new time window is larger than the starting one,
        the trace will be padded with fill_value
        WARNING : the traces are resampled on a constant time grid using linear interpolation !!!
        """

        if not len(self):
            raise EmptyStreamError()

        starttimes = np.asarray([tr.starttime for tr in self], float)
        endtimes = np.asarray([tr.endtime for tr in self], float)
        deltas = np.asarray([tr.delta for tr in self], float)

        delta = np.min(deltas)
        start = np.min(starttimes)
        end = np.max(endtimes)

        new_npts = int(np.floor((end - start) / delta))
        new_time = np.arange(new_npts) * delta + start

        for n, trace in enumerate(self):
            trace: Trace

            if (trace.delta == delta) and \
                    (trace.starttime == start) and \
                    (trace.npts == new_npts):
                # no need to interpolate the signal
                continue

            old_time = trace.atime()
            old_data = trace.data

            trace.data = np.interp(
                new_time, xp=old_time, fp=old_data,
                left=fill_value, right=fill_value)

            trace.starttime = start
            trace.delta = delta

        if qc:
            try:
                self.check_stream_sampling_regularization()
            except (EmptyStreamError, SamplingError) as e:
                e.args = ("the regularization failed, {}".format(str(e)))
                raise e
        return self

    def slide(self,
            winlen: float, winstep: float,
            starttime: Union[float, None] = None,
            endtime: Union[float, None] = None,
            winmode: Union[int, None] = None,
            accuracy: float = 1e-9,
            fixlen: bool = True,
            copy: bool = True,
            verbose: bool = False):
        """
        generate a series of data traces trimmed from self over a slidding window.

        if copy is False, the generated traces contain shallow copies of self.data
        which means that modifying any of these copies will also affect self.data
        and all other overlapping subtraces.
        use it for read-only applications that only need a small data piece
        Only starttime, delta and data will be filled in the shallow copies
        """

        self.check_stream_sampling_regularization()
        delta = self[0].delta
        exepected_npts = int(np.floor(winlen / delta))

        starttimes, endtimes = split_time_into_windows(
            starttime=starttime if starttime is not None else self.get_if_common('starttime'),
            endtime=endtime if endtime is not None else self.get_if_common('endtime'),
            winlen=winlen,
            winstep=winstep,
            winmode=winmode,
            verbose=verbose)

        for t_begin, t_end in zip(starttimes, endtimes):

            substream = Stream([])
            for trace in self:
                trace: Trace
                subtrace = trace.shallow_copy_between(
                    starttime=t_begin,
                    endtime=t_end,
                    accuracy=accuracy)

                if fixlen:
                    if subtrace.npts > exepected_npts:
                        subtrace.data = subtrace.data[:exepected_npts]
                    elif subtrace.npts < exepected_npts:
                        subtrace.pad(npad=exepected_npts - subtrace.npts, value=0.)
                    else:
                        pass
                substream.append(subtrace)

            substream.check_stream_sampling_regularization()
            if copy:
                yield substream.copy()
            else:
                yield substream

    def stack(self):
        try:
            self.check_stream_sampling_regularization()

        except (EmptyStreamError, SamplingError) as e:
            e.args = (f'could not stack the waveforms, reason: {str(type(e))} {str(e)}', )
            raise e
              
        trace = self[0].copy()
        trace.data = np.asarray([tr.data for tr in self]).mean(axis=0)
        return trace

    def phase_weighted_stack(self, pg: float = 0.6, norm_weighting_function: bool = True):

        try:
            self.check_stream_sampling_regularization()

        except (EmptyStreamError, SamplingError) as e:
            e.args = (f'could not stack the waveforms, reason: {str(type(e))} {str(e)}',)
            raise e

        trace = self[0].copy()
        trace.data = pws([tr.data for tr in self], pg=pg, norm_weighting_function=norm_weighting_function)

        return trace

    def mean(self):
        nptss = np.asarray([tr.npts for tr in self], float)
        sum = np.sum([tr.data.sum() for tr in self])
        mean = sum / nptss.sum()
        return mean

    def pseudo_std(self):
        """
        std is evaluated by means of deviations relative to the mean of each trace
        and not relative to the ensemble mean as in self.std
        """
        nptss = np.asarray([tr.npts for tr in self], float)
        covariances = np.asarray([tr.data.std() ** 2.0 for tr in self], float)  # E((Xi - E(Xi))^2)
        return ((nptss * covariances).sum() / nptss.sum()) ** 0.5

    def std(self):
        # return np.concatenate([tr.data for tr in self]).std()

        # same as above without concatenating arrays
        nptss = np.asarray([tr.npts for tr in self], float)
        means = np.asarray([tr.data.mean() for tr in self], float)
        mean = (nptss * means).sum() / nptss.sum()
        deviations = np.array([((tr.data - mean) ** 2.0).sum() for tr in self])
        return (deviations.sum() / nptss.sum()) ** 0.5

    def rms(self):
        mean_square = 0.
        count = 0.
        for tr in self:
            trace_square_sum = (tr.data ** 2.0).sum()
            mean_square = (count * mean_square + trace_square_sum) / (count + tr.npts)
            count += tr.npts

        return np.sqrt(mean_square)

    def clip(self, nstd=10.0):
        """
        remove outliers above a certain threshold given in number of times the pseudo_std
        :param nstd:
        :return:
        """
        means = np.asarray([tr.data.mean() for tr in self], float)
        pseudo_std = self.pseudo_std()
        for tr, m in zip(self, means):
            tr.data = tr.data.clip(m - nstd * pseudo_std, m + nstd * pseudo_std)

    def show(self, ax: Union[None, plt.Axes]=None, **kwargs):

        """
        show many traces on same plot with vertical offset 1 per trace
        """
        if ax is None:
            ax = plt.gca()

        show_stream(stream=self, ax=ax, **kwargs)
        return self

    def pick(self, ax, save_stream_as: Union[str, None]=None, **kwargs):
        from seiscod.picker import StreamPicker, DEFAULT_TIMEPICK

        swapxy = kwargs.setdefault('swapxy', False)
        # ydim = kwargs.setdefault('ydim', 'trace')

        # if ydim != "trace":
        #     raise NotImplementedError('ydim other than trace is not implemented for picking')

        # timepicks = np.asarray([tr.timepick if hasattr(tr, "timepick") else DEFAULT_TIMEPICK for tr in self])

        # display the stream

        trace_offsets = show_stream(stream=self, ax=ax, **kwargs)
        # create the picker and connect it (connection done by the __init__ method)
        StreamPicker(
            ax=ax, stream=self, trace_offsets=trace_offsets, verbose=True,
            swapxy=swapxy,
            save_stream_as=save_stream_as)
        # add the existing picks if any => in __init__
        # start the picking session => in __init__
        plt.show()

        # timepicks, traceindexs = picker.collect_picks()
        # self.set('timepick', DEFAULT_TIMEPICK * np.ones(len(self)))
        # for timepick, traceindex in zip(timepicks, traceindexs):
        #     self[traceindex].__setattr__('timepick', timepick)

        return self

    def shade(self,
              ax: Union[None, plt.Axes] = None,
              cmap: Union[None, Colormap] = None,
              vmin: Union[None, float] = None, vmax: Union[None, float] = None,
              powergain: float = 1.,
              seedticks: bool = False, timeticks: bool = False,
              showcolorbar: bool = True, swapxy: bool = False,
              ydim: str = "trace",
              **kwargs):
        """
        """
        if ax is None:
            ax = plt.gca()

        shade_stream(
            stream=self,
            ax=ax,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            powergain=powergain,
            seedticks=seedticks,
            timeticks=timeticks,
            showcolorbar=showcolorbar,
            swapxy=swapxy,
            ydim=ydim,
            **kwargs)
        return self

    def to_npz(self, npzfilename: str, additional_keys: Union[None, str, list, np.ndarray] = "*"):
        """
        write the stream under npz format
        :param npzfilename: filename, must end with .seiscodstream.npz
        :param additional_keys: by default only a few attributes are saved in the npz file
            it is possible to save more attributes by mentionning their name in this list
            the attributes must exist in all traces (obtained using Stream.get)
        :return:
        """
        if not len(self):
            raise EmptyStreamError

        write_npz(
            seiscodstream=self,
            npzfilename=npzfilename,
            additional_keys=additional_keys)

        return self

    def from_raw_trace_list(self, raw_trace_list: list):
        for raw_trace in raw_trace_list:
            trace = Trace().from_raw_trace(raw_trace)
            self.append(trace)
        return self

    def from_npz(self, npzfilename: str, headonly: bool=False,
            additional_keys: Union[None, list, np.ndarray, str] = None,
            trace_selector: Union[None, types.FunctionType] = None,
            trace_indexs: Union[None, list, slice] = None):

        npzreader = NPZReader(npzfilename=npzfilename)

        npzreader.load(
            headonly=headonly, additional_keys=additional_keys,
            trace_selector=trace_selector, trace_indexs=trace_indexs)

        # if headonly, the data is not in raw_traces because headonly passed to npzreader.load
        self.from_raw_trace_list(npzreader.raw_trace_list)

        return self

    def from_seg2_using_pyseg2(self, seg2file: str):
        """
        experimental, use with care
        """

        from pyseg2.seg2file import Seg2File, Seg2Trace
        seg2 = Seg2File()
        with open(seg2file, 'rb') as fid:
            seg2.load(fid)

        for seg2trace in seg2.seg2traces:
            seg2trace: Seg2Trace

            trace = Trace(
                starttime=0.,
                delta=1.0,
                npts=seg2trace.trace_data_block.data.size,
                data=seg2trace.trace_data_block.data,
                )

            trace.delta = None
            for string in seg2trace.trace_free_format_section.strings:
                if string.key == "SAMPLE_INTERVAL":
                    trace.delta = float(string.value)

                elif string.key == "NOTE":
                    trace.__setattr__(string.key, string.value.split(';'))

                else:
                    trace.__setattr__(string.key, string.value)

            if trace.delta is None:
                raise KeyError('SAMPLE_INTERVAL not found')

            self.append(trace)
        return self

    def from_seg2_using_obspy(self, seg2file: str):
        from seiscod.readwrite.seg2.readseg2withobspy import SEG2ForSeispyReader  # NOT IN THE MAIN IMPORTS !

        seg2reader = SEG2ForSeispyReader()
        raw_trace_list = seg2reader.read_file(seg2file)
        self.from_raw_trace_list(raw_trace_list)
        return self

    def from_segy_using_obspy(self,
        segyfile: str,
        segy_keys_to_load: Union[None, list, np.ndarray, str] = None,
        trace_indexs: Union[list, np.ndarray, None]=None,
        segy_keys_for_data_selection: Union[None, list, np.ndarray, str] = None,
        segy_keys_min_values: Union[None, list, np.ndarray] = None,
        segy_keys_max_values: Union[None, list, np.ndarray] = None,
        # trace_selector: Union[callable, None]=None,
        headonly: bool=False,
        endian=None,
        ):
        """
        :param segyfile: name of the segy file to read
        :param segy_keys_to_load: list of segy keys among
            obspy.io.segy.header.TRACE_HEADER_KEYS + "starttime" or "*" or None
        :param trace_indexs: list of indexs from 0, with the traces indexs to read
        :param segy_keys_for_data_selection: used only if trace_indexs is None,
            list of segy keys among
            obspy.io.segy.header.TRACE_HEADER_KEYS
            to use for the data selection by trace_selector
        :param segy_keys_min_values: minimum value to select, length must match segy_keys_for_data_selection
        :param segy_keys_max_values: maximum value to select, length must match segy_keys_for_data_selection
        :param headonly: if True, the data is packed in the output stream
        :return self: self
        """
        from seiscod.readwrite.segy.readsegyusingobspy import SegyReaderUsingObspy  # NOT IN THE MAIN IMPORTS !

        if trace_indexs is not None:
            # segy_keys_for_data_selection is ignored
            # trace_selector is ignored

            segy_reader = SegyReaderUsingObspy(
                segyfile=segyfile,
                segy_keys=None,
                endian=endian)

            raw_trace_list = segy_reader.unpack_traces(
                trace_indexs=trace_indexs,
                segy_keys=segy_keys_to_load,
                headonly=headonly)

        elif segy_keys_for_data_selection is not None:
            assert len(segy_keys_for_data_selection) == \
                len(segy_keys_min_values) == \
                len(segy_keys_max_values)

            segy_reader = SegyReaderUsingObspy(
                segyfile=segyfile,
                segy_keys=segy_keys_for_data_selection,
                endian=endian)

            trace_indexs = segy_reader.select_trace_indexs_using_ranges(
                segy_keys=segy_keys_for_data_selection,
                min_values=segy_keys_min_values,
                max_values=segy_keys_max_values,
                )

            raw_trace_list = segy_reader.unpack_traces(
                trace_indexs=trace_indexs,
                segy_keys=segy_keys_to_load,
                headonly=headonly)

        else:
            # raise NotImplementedError('trace_indexs or segy_keys_for_data_selection is required')
            # load the whole file, may take long time
            segy_reader = SegyReaderUsingObspy(
                segyfile=segyfile,
                segy_keys=None,
                endian=endian)

            trace_indexs = np.arange(segy_reader.ntraces)

            raw_trace_list = segy_reader.unpack_traces(
                trace_indexs=trace_indexs,
                segy_keys=segy_keys_to_load,
                headonly=headonly)

        self.from_raw_trace_list(raw_trace_list)
        return self

    def from_segd(self, segdfilename: str, headonly: bool=False, ):
        from seiscod.readwrite.segd.readsegd1 import read_segd

        raw_trace_list = read_segd(
            filename=segdfilename,
            headonly=headonly,
            indexs=None,
            )

        for raw_trace in raw_trace_list:
            # move attributes from ['segd'] to root attributes
            try:
                for key, val in raw_trace.trace_dict['segd'].items():
                    raw_trace.trace_dict[key] = val

                raw_trace.trace_dict.__delitem__('segd')
            except KeyError:
                pass

            raw_trace.trace_dict['starttime'] = raw_trace.trace_dict['starttime'].timestamp

            trace = Trace().from_raw_trace(raw_trace)
            self.append(trace)

        return self

    def from_tusmus(self, tusfilename: str, musfilename: Union[str, None]=None):

        from seiscod.readwrite.tusmus.readtusmus \
            import read_tus_mus, MusChannelError

        raw_trace_list = []
        for channel in range(10000):
            try:
                raw_trace = read_tus_mus(
                    tus_file=tusfilename,
                    mus_file=musfilename,
                    channel=channel,
                    )
            except MusChannelError:
                break

            raw_trace_list.append(raw_trace)
        self.from_raw_trace_list(raw_trace_list)
        return self

    def from_sig(self, sigfilename: str):
        from seiscod.readwrite.sig.readsig import read_sig
        raw_trace = read_sig(
            filename=sigfilename,
            zero_at_trigger_time=True,
            )
        trace = Trace().from_raw_trace(raw_trace)
        self.append(trace)
        return self

    def from_mseed(self, mseedfilename: str, nsegment: int = -1, unpack_data: bool = True):
        try:
            from rmseed import SeedReader
        except ImportError:
            raise ImportError('rmseed not installed')
        # trick to prevent c-allocated memory to be freed when leaving this function (by garbage collector)
        global segments

        sr = SeedReader()

        segments = sr.read(mseedfile=mseedfilename, nsegment=nsegment, unpack_data=unpack_data)

        for segment in segments:
            trace = Trace()
            trace.from_rmseed_segment(segment)
            self.append(trace)

        return self

    def set(self, key, values):

        if hasattr(values, '__iter__'):
            if not len(values) == len(self):
                raise ValueError('values must be a scalar or an iterable with same length as self')
            for trace, val in zip(self, values):
                trace.__setattr__(key, val)
        else:
            for trace in self:
                trace.__setattr__(key, values)

    def apply(self, output_key:str, fun, input_keys:Union[str, List[str]]):
        """
        set an attribute based on a function of others
        e.g.

        stream.apply(
            'seedid',
            lambda network, station, location, channel: '%s.%s.%s.%s' % (network, station, location, channel),
            ['network', 'station', 'location', 'channel'],
            )

        will set seedids by concatenating network station ... attributes
        """
        if isinstance(input_keys, str):
            input_keys = [input_keys]
        args_list = zip(*[self.get(key) for key in input_keys])
        self.set(output_key, [fun(*args) for args in args_list])

    def get(self, key):
        """
        extract a given trace attribute across all the traces of the stream
        and store it into a numpy array
        """

        if not len(self):
            raise EmptyStreamError

        if key == "data":
            if self.is_regularized():
                return np.asarray([trace.data for trace in self])
            else:
                return [trace.data for trace in self]


        try:
            values = np.array([trace.__getattribute__(key) for trace in self])

        except (AttributeError, KeyError) as e:
            message = "key {} was not found in " \
                      "the attributes of class {}".format(
                key, type(self[0]))
            e.args = (message, )
            raise e

        return values

    def get_if_common(self, key, default=None, raise_if_non_unique: bool=True):
        """
        extract a scalar value for an attribute only if it is the same for all traces in the stream
        otherwise, raise AttributeError or return default value
        """
        values = self.get(key)
        if np.all(values[1:] == values[0]):
            return values[0]
        elif raise_if_non_unique:
            raise AttributeError(f'the values of {key} are not the same for all traces')
        else:
            return default

    def isort(self, indexs: Union[list, np.ndarray]):
        assert len(indexs) == len(self)
        assert (np.arange(len(self)) == np.sort(indexs)).all()
        # == update the object
        self.__init__([self[i] for i in indexs])
        return self  # so that methods can be queued


    def lexsort_by(self, keys: list):

        list_of_values = [self.get(key) for key in keys[::-1]]
        i_sort = np.lexsort(list_of_values)

        return self.isort(indexs=i_sort)


    def sort_by(self, key, order=1):
        if not order in [1, -1]:
            raise ValueError

        # == extract sorting value
        values = self.get(key)

        # == order by sorting value
        i_sort = np.argsort(values)
        if order == -1:
            i_sort = i_sort[::-1]

        return self.isort(indexs=i_sort)

    def group_by_values(self, values: np.ndarray):
        """
        group traces having similar values in the values array
        """
        assert len(values) == len(self)

        stream_groups = {}
        for trace, value in zip(self, values):
            try:
                stream_groups[value].append(trace)
            except KeyError as e:
                stream_groups[value] = Stream([trace])

        return stream_groups

    def group_by(self, key: str):
        """
        group traces according to key,
        return a dictionnary with one item per group,
        group of traces are stored as Stream objects

        example: group by seedid

        dictionary = st.group_by('seedid')
        for seedid, group_stream in dictionary.items():
            print('# === seedid:', seedid)
            for trace in group_stream:
                print(trace)

        """
        return self.group_by_values(values=self.get(key))

    def group_by_many(self, keys: list):
        """
        group traces according to key,
        return a dictionnary with one item per group,
        group of traces are stored as Stream objects

        example: group traces having same seedid and delta

        dictionary = st.group_by_many(keys = ['seedid', 'delta'])
        for (seedid, delta), group_stream in dictionary.items():
            print('# === seedid, delta:', seedid, delta)
            for trace in group_stream:
                print(trace)

        """
        values = [self.get(key) for key in keys]
        value_tuples = list(zip(*values))
        return self.group_by_values(values=value_tuples)

    def stack_on(self, keys: list, pws: float = 1.0):
        """
        stack traces having common values for all fields listed in keys
        :param keys: list of keys to use to group traces together and stack them
        :param pws: 1.0 for regular stack, other value for phase weighted stack
        :return:
        """
        if isinstance(keys, str):
            raise TypeError("list of keys not key", type(keys))

        stack_traces = []
        for keytuple, group_stream in self.group_by_many(keys=keys).items():
            if pws == 1.0:
                trace_stack = group_stream.stack()
            else:
                trace_stack = group_stream.phase_weighted_stack(pg=pws, norm_weighting_function=True)
            stack_traces.append(trace_stack)
        self.__init__(traces=stack_traces)
        return self

    def clustering(self, n_clusters: int = 5, **kwargs):
        """
        :param n_clusters: 
        :param whiten: 
        :return: stream_clusters = a stream with the centroid traces
                 self: each trace in self has been equiped with a "cluster_index"
                       attribute which refers to the items of stream_clusters
        """
        self.check_stream_sampling_regularization()
        delta = self.get_if_common('delta')
        starttime = self.get_if_common('starttime')

        data_traces = np.asarray([tr.data for tr in self])
        correlation_matrix = waveform_corr_coeff(data_traces=data_traces)
        condensed_distances = waveform_distances(correlation_matrix=correlation_matrix, power=0.1)

        cluster_masters, cluster_affiliations, cluster_counts, clustering_index = \
            waveform_clustering(
                data_traces=data_traces,
                condensed_distances=condensed_distances,
                n_clusters=n_clusters,
                sort_by="count")

        master_traces = Stream()
        for n_cluster in range(n_clusters):
            tr_master = Trace(
                data=cluster_masters[n_cluster, :],
                delta=delta, starttime=starttime, seedid=f"cluster_{n_cluster}")
            tr_master.cluster_number = n_cluster
            tr_master.cluster_count = cluster_counts[n_cluster]
            master_traces.append(tr_master)

        for n, tr in enumerate(self):
            tr.cluster_number = cluster_affiliations[n]
            tr.cluster_count = cluster_counts[tr.cluster_number]
            tr.clustering_index = clustering_index[n]

        # return stream_of_masters, self
        return self, master_traces, correlation_matrix

    def select(self, mask: np.array, inplace: bool=False):
        """
        mask: boolean array with same length as self or index array
        return a selection of traces (shallow copy)
        if you need a deep copy, do it yourself with copy() after select
        """
        r = np.arange(len(self))[mask]  # convert to indexes
        if inplace:
            self.__init__([self[i] for i in r])
        else:
            return Stream([self[i] for i in r])

    # ============ unit selection methods that can be queued
    def select_eq(self, key, value, inplace: bool=False):
        return self.select(self.get(key) == value, inplace=inplace)

    def select_in(self, key, values, inplace: bool=False):
        return self.select(np.in1d(self.get(key), values), inplace=inplace)

    def select_neq(self, key, value, inplace: bool=False):
        return self.select(self.get(key) != value, inplace=inplace)

    def select_ge(self, key, value, inplace: bool=False):
        return self.select(self.get(key) >= value, inplace=inplace)

    def select_le(self, key, value, inplace: bool=False):
        return self.select(self.get(key) <= value, inplace=inplace)

    def select_gt(self, key, value, inplace: bool = False):
        return self.select(self.get(key) > value, inplace=inplace)

    def select_lt(self, key, value, inplace: bool = False):
        return self.select(self.get(key) < value, inplace=inplace)

    def reject_seedids(self, seedids):
        if not len(self):
            raise EmptyStreamError

        trace_seedids = np.array([trace.seedid for trace in self], str)
        bad_traces = np.in1d(trace_seedids, seedids)

        self.__init__([self[i] for i in
                       range(len(self))
                       if not bad_traces[i]])
        return self  # so that methods can be queued

    def reject_nulls(self):
        seedids = self.get('seedid')
        bad_traces = np.array([(tr.data == 0.).all() for tr in self], bool)
        null_seedids = seedids[bad_traces]
        self.reject_seedids(null_seedids)
        return null_seedids

    # IN PLACE OPERATIONS
    def lowpass(self, *args, **kwargs):
        for trace in self:
            trace: Trace
            trace.lowpass(*args, **kwargs)
        return self

    def highpass(self, *args, **kwargs):
        for trace in self:
            trace: Trace
            trace.highpass(*args, **kwargs)
        return self

    def bandpass(self, *args, **kwargs):
        for trace in self:
            trace: Trace
            trace.bandpass(*args, **kwargs)
        return self

    def gaussbandpass(self, *args, **kwargs):
        for trace in self:
            trace: Trace
            trace.gaussbandpass(*args, **kwargs)
        return self

    def gaussbandstop(self, *args, **kwargs):
        for trace in self:
            trace.gaussbandstop(*args, **kwargs)
        return self

    def next_fast_len(self):
        for trace in self:
            trace.next_fast_len()
        return self

    def fft(self):
        for trace in self:
            try:
                trace.fft()
            except TypeError:
                pass

        return self

    def ifft(self):
        for trace in self:
            try:
                trace.ifft()
            except TypeError:
                pass
        return self

    def norm(self, *args, **kwargs):
        for trace in self:
            trace.norm(*args, **kwargs)
        return self

    def multipro_any_output(
            self,
            func: Union[types.FunctionType, types.MethodType],
            ncpu: Union[int, None] = None) -> list:

        """
        run func on every traces in self in parallel
        func must take a trace object as input and can return any kind of object

        def func(trace):
            ... do anything with trace ...
            return something
        """
        if ncpu is None:
            ncpu = cpu_count()
        with Pool(ncpu) as p:
            outputs = p.map(func=func, iterable=self)
        return outputs

    def multipro(self, func: types.FunctionType, ncpu=None):
        """
        run func on every traces in self in parallel
        func must take a trace object as input and output a trace object

        def func(trace):
            trace.do_this()
            trace.do_that()
            return trace
        """
        traces = self.multipro_any_output(func=func, ncpu=ncpu)
        self.__init__(traces)
        return self

    def __getitem__(self, item):
        """experimental : overwrite the default list behavior to return a Stream (shallow copy)"""
        traces = list.__getitem__(self, item)
        if isinstance(traces, list):
            return Stream(traces=traces)

        elif isinstance(traces, (Trace, FFTTrace)):
            return traces

        else:
            raise NotImplementedError(type(traces))


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    stream = Stream([])
    for _ in range(10):
        tr = Trace(
            seedid=str(int(np.random.rand() * 1.e4)),
            delta=0.4 + 0.1 * np.random.rand(),
            starttime=1000. + 10 * np.random.randn(),
            data=np.random.randn(int(2500 + np.random.randn() * 10)))
        tr.bandpass(0.01, 0.5, 4, True)
        stream.append(tr)

    print(stream)

    stream.show(plt.gca(), gain=0.1, color="k")

    # plt.show()

    dtype = stream.check_data_types()

    oldstd = stream.std()
    stream.regularize(qc=True)
    newstd = stream.std()

    stream.show(plt.gca(), gain=0.1 * newstd / oldstd, color="r", obspy_decim=True)
    stream.to_npz('toto.seiscodstream.npz')
    del stream
    stream = Stream([])
    stream.from_npz('toto.seiscodstream.npz')

    # plt.show()
    stream.show(plt.gca(), gain=0.1 * newstd / oldstd, color="g", linestyle="--")
    print(stream)

    plt.show()
