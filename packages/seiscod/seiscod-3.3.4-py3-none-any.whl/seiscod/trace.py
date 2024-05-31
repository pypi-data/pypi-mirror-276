# built in
from typing import Union
from copy import deepcopy
import warnings

# official dependencies
import numpy as np
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy.fftpack import fft, ifft, fftfreq, next_fast_len

# internal imports
from tempoo.timetick import timetick
from tempoo.windows import split_time_into_windows
from seiscod.signal.taper import cos_taper_width, cos_taper_four_points
from seiscod.signal.butter import ButterworthFilter
from seiscod.signal.hypermax import hyperzeros, hypermax, isolate_sections_with_same_sign
from seiscod.signal.parseval import time_energy, fft_energy
from seiscod.signal.fsmooth import fsmooth1
from seiscod.signal.spectralwhitening import spectral_whitening, power_whitening
from seiscod.signal.dominantfreq import dominant_frequency
# from seiscod.filter.butter import lowpass, highpass, bandpass
# from seiscod.filter.taper import costaperwidth
from seiscod.readwrite.rawtrace import RawTrace
from seiscod.errors import StarttimeError, SamplingRateError, NptsError
from seiscod.sampling import trim_data

"""
Simplified objects for trace and stream without obspy 
"""


class Trace(object):
    header_keys = ['seedid', 'delta', 'starttime', 'longitude', 'latitude', 'elevation', 'distance']
    data_keys = ['data']
    # additional_keys = []  # is a property not a physical attribute

    def __init__(self, seedid: str = "",
                 delta: float = 1.,
                 starttime: float = 0.0,
                 longitude: float = 0.0,
                 latitude: float = 0.0,
                 elevation: float = 0.0,
                 distance: float = 0.0,
                 data: np.ndarray = np.array([], np.dtype('float64')),
                 **ignored):

        self.seedid: str = seedid
        self.delta: float = delta
        self.starttime: float = starttime
        self.longitude: float = longitude
        self.latitude: float = latitude
        self.elevation: float = elevation
        self.distance: float = distance
        self.data: np.ndarray = data

    @property
    def additional_keys(self):
        _additional_keys = []
        for key in self.__dict__.keys():
            if key in self.header_keys:
                continue
            elif key in self.data_keys:
                continue
            elif key.startswith('_'):
                continue
            _additional_keys.append(key)
        return _additional_keys

    def __str__(self):
        return 'seedid:{} npts:{} delta:{}s starttime:{}s'.format(
            self.seedid,
            self.npts,
            self.delta,
            self.starttime)

    def __repr__(self):
        return self.__str__()

    def copy(self, data=True, header=True, additional=True):
        """
        uncopied attributes will be reset to their default value
        """
        if data and header and additional:
            return deepcopy(self)

        elif not data and not header and not additional:
            raise ValueError

        tr = Trace()
        self_header_keys = self.header_keys
        self_data_keys = self.data_keys
        self_additional_keys = self.additional_keys
        for key, value in self.__dict__.items():
            if header and key in self_header_keys:
                tr.__setattr__(key, deepcopy(value))

            elif data and key in self_data_keys:
                tr.__setattr__(key, deepcopy(value))

            elif additional and key in self_additional_keys:
                tr.__setattr__(key, deepcopy(value))

        return tr

    @property
    def npts(self):
        return len(self.data)

    @property
    def endtime(self):
        return self.starttime + (self.npts - 1) * self.delta

    def from_obspy(self, trace,
            additional_keys=None,
            segy_keys=None, su_keys=None, seg2_keys=None):
        """
        :param trace: obspy.trace.Trace used to populate this object
        :return:
        """
        try:
            # I don't want anything from obspy in the top imports !!!
            # this may fuck up matplotlib behavior
            from obspy.io.segy.header import TRACE_HEADER_KEYS as SEGY_TRACE_HEADER_KEYS
        except ImportError as e:
            e.args = ('obspy is required for this funciton', )
            raise e

        self.seedid = "{network}.{station}.{location}.{channel}".format(**trace.stats)
        self.delta = trace.stats.delta
        self.starttime = trace.stats.starttime.timestamp
        self.data = trace.data

        # if hasattr(trace.stats, 'coordinates'):
        #     # default coordinates attributes of seiscod
        #     for key in ['longitude', 'latitude', 'elevation', 'distance']:
        #         if hasattr(trace.stats.coordinates, key):
        #             try:
        #                 self.__setattr__(key, trace.stats.coordinates[key])
        #
        #             except (AttributeError, NameError, KeyError) as e:
        #                 warnings.warn(f'could not set attribute {key}: >{str(e)}<')

        if additional_keys is not None:
            for key, val in trace.stats.items():
                if key in additional_keys:
                    try:
                        self.__setattr__(key, val)
                    except (KeyError, AttributeError):
                        self.__setattr__(key, None)

        if segy_keys is not None and hasattr(trace.stats, 'segy'):
            if segy_keys == "*":
                assert len(SEGY_TRACE_HEADER_KEYS) > 0
                segy_keys = SEGY_TRACE_HEADER_KEYS
    
            for key in segy_keys:
                if key == "offset":
                    # obspy name is too looooooooooooooooooong
                    obspy_key = "distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group"
                else:
                    obspy_key = key
                    
                self.__setattr__(key, trace.stats.segy.trace_header[obspy_key])

        if su_keys is not None:
            raise NotImplementedError

        if seg2_keys is not None:
            raise NotImplementedError

        return self
    
    def to_obspy(self):
        """
        :return data, header: objects to use if you need to initate an obspy.trace.Trace
        """
        # warning this module must keep independant from obspy, I just assume here that the user is
        # trying to convert this object to obspy, so obspy is supposed to be installed
        try:
            from obspy.core.trace import Trace as ObspyTrace, UTCDateTime as ObspyUTCDateTime
        except ImportError as e:
            e.args = ('obspy not installed', )
            raise e

        try:
            network, station, location, channel = self.seedid.split('.')
        except ValueError:
            # seedid string is not formatted as expected, quick fix
            network, station, location, channel = "", self.seedid, "", ""
            
        header = {"network": network,
                  "station": station,
                  "location": location,
                  "channel": channel,
                  "delta": self.delta,
                  "starttime": ObspyUTCDateTime(self.starttime),
                  "seiscod": {
                      "longitude": self.longitude,
                      "latitude": self.latitude,
                      "elevation": self.elevation,
                      "distance": self.distance,
                      **{key: getattr(self, key) for key in self.additional_keys},
                      },
                  }

        return ObspyTrace(self.data, header)

    def from_rmseed_segment(self, segment):
        self.seedid = segment.seedid
        self.delta = 1. / segment.sprate
        self.starttime = segment.starttime
        self.data = segment.data

    def from_raw_trace(self, raw_trace: RawTrace):
        for key, val in raw_trace.trace_dict.items():
            if key == "npts":
                continue
            self.__setattr__(key, val)
        self.data = raw_trace.trace_data
        return self

    def rtime(self):
        return np.arange(self.npts) * self.delta

    def atime(self):
        # ISSUE : if starttime is huge (timestamp) and delta very small (like micro seconds)
        # then the result might be inaccurate
        return self.starttime + self.rtime()

    def energy(self):
        return time_energy(time_data=self.data, delta=self.delta)

    def obspy_like_decim(self, nwin=1000):
        """obspy-like data decimation for display (and only for display)"""
        t = self.atime()
        d = self.data
        if self.npts <= nwin:
            return t, d

        n_per_win = self.npts // nwin
        nwin = self.npts // n_per_win
        remain = self.npts % n_per_win
        npad = n_per_win - remain
        if npad:
            nwin += 1

        lwin = n_per_win * self.delta

        assert self.npts + npad == n_per_win * nwin
        assert npad < n_per_win, (self.npts, nwin, n_per_win, npad)
        d = np.concatenate((self.data,
                        self.data[-1] * np.ones(npad, self.data.dtype)))

        d = d.reshape((nwin, n_per_win))
        min_values = d.min(axis=1)
        max_values = d.max(axis=1)

        values = np.zeros(2 * nwin + 2, d.dtype)
        timestamps = np.zeros(2 * nwin + 2, t.dtype)

        values[1:-1:2] = max_values
        values[2::2] = min_values
        values[0] = self.data[0]
        values[-1] = self.data[-1]
        timestamps[0] = self.starttime
        timestamps[1:-1:2] = timestamps[2::2] = \
            self.starttime + np.arange(nwin) * lwin + 0.5 * lwin
        timestamps[-3:] = self.endtime

        return timestamps[:-1], values[:-1]

    def obspy_like_show(self, ax, nwin=1000, timeticks=True, *args, **kwargs):
        timestamps, values = self.obspy_like_decim(nwin)
        hdl = ax.plot(timestamps, values, *args, **kwargs)
        if timeticks:
            timetick(ax=ax, axis="x", major=True, minor=True)
        return hdl

    def show(self, ax: Union[None, plt.Axes]=None,
             timeticks: bool = True,
             facealpha: float = 0.,
             facecolor: str = "rb",
             *args, **kwargs):

        if ax is None:
            ax = plt.gca()

        t = self.atime()
        if facealpha == 0:
            hdl = ax.plot(t, self.data, *args, **kwargs)

        elif 0 < facealpha <= 1.0:

            if len(facecolor) == 2:
                twocolors = True
                colorsup = facecolor[0]
                colorinf = facecolor[1]
            elif len(facecolor) == 1:
                twocolors = False
                colorsup = facecolor[0]
                colorinf = None
            else:
                raise ValueError(facecolor)

            face_segments = []
            face_colors = []
            for s, tim, dat in isolate_sections_with_same_sign(t, self.data, assume_t_growing=True):
                if s >= 0:
                    face_segments.append(np.column_stack((tim, dat)))
                    face_colors.append(colorsup)
                elif s < 0 and twocolors:
                    face_segments.append(np.column_stack((tim, dat)))
                    face_colors.append(colorinf)
            coll = PolyCollection(face_segments,
                                  facecolors=face_colors,
                                  alpha=facealpha)

            hdl = ax.plot(t, self.data, *args, **kwargs)
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            ax.add_collection(coll)
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            hdl = (hdl, coll)
        else:
            raise ValueError(facealpha)

        # if np.sign(t[0]) * np.sign(t[-1]) > 0:
        if timeticks:
            timetick(ax=ax, axis="x", major=True, minor=True)

        return hdl

    # ======================= CLASS CONVERSIONS
    def to_fourier(self, copy=False):
        warnings.warn('Trace.to_fourier is obsolet, please use Trace.fft')
        tr = FFTTrace(
            seedid=self.seedid,
            delta=self.delta,
            starttime=self.starttime,
            longitude=self.longitude,
            latitude=self.latitude,
            elevation=self.elevation,
            distance=self.distance,
            data=fft(self.data))
        if copy:
            return tr.copy()
        return tr

    def pad(self, npad: int, value=0):
        """
        :param npad: the number of samples to add at the end of the signal
        :param value: the padding value
        :param reset_pad_counter:
        :return: self
        """
        if npad < 0:
            raise ValueError(f'pad cannot be negative ({npad})')

        elif npad > 0:
            self.data = np.hstack((self.data, value * np.ones(npad, self.data.dtype)))

        return self

    def padto(self, npts: int, **kwargs):
        """
        :param npts: the desired number of samples, must be higher than self.npts
        :param kwargs: see self.pad
        :return: self
        """
        return self.pad(npad=npts-self.npts, **kwargs)

    def next_fast_len(self, value=0.):
        """NB if self.npts is alread a power of two, then no padding will be applied"""
        npad = next_fast_len(self.npts) - self.npts
        return self.pad(npad, value=value)

    def fft(self):
        """Cast this trace into a FFTTrace. call fft on trace.data"""
        if not isinstance(self, Trace):
            raise TypeError('type is not Trace')
        if isinstance(self, FFTTrace):
            return self

        self.__class__ = FFTTrace
        if len(self.data):
            self.data = fft(self.data)

        assert isinstance(self, FFTTrace)
        return self

    # ======================= TYPE CONVERSIONS
    # applied "in place", return self so that methods can be queued like
    # [tr.do_this().do_that() for tr in stream]
    def float64(self):
        self.data = self.data.astype(np.dtype('float64'))
        return self

    def float32(self):
        self.data = self.data.astype(np.dtype('float32'))
        return self

    # ======================= PROCESSING
    # applied "in place", return self so that methods can be queued like
    # [tr.do_this().do_that() for tr in stream]
    def detrend(self):
        t = self.rtime()
        self.data -= np.polyval(np.polyfit(t, self.data, deg=1), t)
        return self

    def edge_detrend(self, width):
        n = int(width // self.delta)
        if n < 1:
            raise ValueError("width too short", width)
        b = np.median(self.data[:n])
        e = np.median(self.data[-n:])
        self.data -= (e - b) * np.linspace(0, 1, self.npts, dtype=self.data.dtype) + b
        return self

    def taperbetween(self, tmin: float, tmax: float, width: float):
        raise NotImplementedError

    def taperfourpoints(self, t0, t1, t2, t3):
        tap = cos_taper_four_points(
            starttime=self.starttime,
            npts=self.npts,
            sampling_rate=1./self.delta,
            t0=t0, t1=t1, t2=t2, t3=t3)
        self.data *= tap
        return self

    def taperwidth(self, width, left=True, right=True):
        tap = cos_taper_width(
            npts=self.npts,
            sampling_rate=1. / self.delta,
            width=width, dtype=self.data.dtype,
            left=left, right=right)
        self.data *= tap
        return self

    def trim(self,
             starttime: Union[float, None],
             endtime: Union[float, None],
             fill_value: float = 0.,
             accuracy: float = 1e-9):
        """
        trim the data array in place
        """

        assert self.npts == len(self.data)

        new_starttime, new_data = \
            trim_data(
                current_starttime=self.starttime,
                delta=self.delta,
                data=self.data,
                required_starttime=starttime,
                required_endtime=endtime,
                fill_value=fill_value,
                accuracy=accuracy,
                copy=False)  # try to avoid the deep copy

        # the new_data array is potentially a shallow copy of self.data (in trimming mde)
        # by overwriting self.data by new_data, there are no risks that the user
        # is suprized by the shallow copy

        self.data = new_data
        self.starttime = new_starttime
        assert self.npts == len(self.data)
        return self

    def data_copy_between(self,
                     starttime: Union[float, None],
                     endtime: Union[float, None],
                     fill_value: float = 0.,
                     accuracy: float = 1e-9):
        """
        simplify to following

        tr.copy().trim(tb, te)
            => means copy all the tr.data array and then isolate the part between tb and te

        tr.data_copy_between(tb, te)
            => does the same but only the data between tb and te is copied

        """
        assert not isinstance(self, FFTTrace)
        assert self.npts == len(self.data)

        new_starttime, new_data = \
            trim_data(
                current_starttime=self.starttime,
                delta=self.delta,
                data=self.data,
                required_starttime=starttime,
                required_endtime=endtime,
                fill_value=fill_value,
                accuracy=accuracy,
                copy=True)

        # copy all fields except data
        copy = self.copy(data=False)

        # whatever window parameters, the new_data is a copy of self.data
        # => user can safely modify copy.data without affecting self.data
        copy.starttime = new_starttime
        copy.data = new_data

        return copy

    def shallow_copy_between(self,
            starttime: Union[float, None],
            endtime: Union[float, None],
            accuracy: float = 1e-9):
        """
        in trim mode, it is possible to obtain a shallow copy of self.data and pack it into a Trace object
        so the user could work on a small data section of self using the methods of Trace
        this method cannot be used in padding mode, so the boudaries are adjusted
        and fill_value makes no sense

        modifying shallow_copy.data will also affect the corresponding segment in self.data
        """

        # shallow copy can only be obtained in trimming mode, adjust the bounds
        if starttime is not None:
            starttime = max([self.starttime, starttime])

        if endtime is not None:
            endtime = min([self.endtime, endtime])

        new_starttime, new_data = \
            trim_data(
                current_starttime=self.starttime,
                delta=self.delta,
                data=self.data,
                required_starttime=starttime,
                required_endtime=endtime,
                # fill_value=fill_value,
                accuracy=accuracy,
                copy=False)

        shallow_copy = Trace(
            seedid=self.seedid,
            delta=self.delta,
            starttime=new_starttime,
            data=new_data)

        return shallow_copy

    def slide(self,
            winlen: float, winstep: float,
            starttime: Union[float, None] = None,
            endtime: Union[float, None] = None,
            winmode: Union[int, None] = None,
            accuracy: float = 1e-9,
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

        starttimes, endtimes = split_time_into_windows(
            starttime=starttime if starttime is not None else self.starttime,
            endtime=endtime if endtime is not None else self.endtime,
            winlen=winlen,
            winstep=winstep,
            winmode=winmode,
            verbose=verbose)

        for t_begin, t_end in zip(starttimes, endtimes):
            tr = self.shallow_copy_between(
                starttime=t_begin,
                endtime=t_end,
                accuracy=accuracy)

            if copy:
                yield tr.copy()
            else:
                yield tr

    def running_average(self, width, shift=False):

        nwin_half = int((width / 2.0) // self.delta)
        nwin = 2 * nwin_half  # even

        # trapeze integration
        data_integral = np.zeros_like(self.data)
        data_integral[1:] = 0.5 * (self.data[1:] + self.data[:-1]).cumsum() * self.delta

        # begin and end of the integration window
        b = (np.arange(self.npts) - nwin_half).clip(0, self.npts-1)
        e = (np.arange(self.npts) + nwin_half).clip(0, self.npts-1)

        # differentiate between begin and end point
        self.data = (data_integral[e] - data_integral[b]) / ((e - b) * self.delta)

        if shift:
            self.starttime += nwin_half * self.delta
        return self

    def stalta(self, sta: float, lta: float):
        """
        :param sta:
        :param lta:
        :param trigger_start:
        :return:
        """
        assert lta > sta > 0.0, ValueError(lta, sta)
        # assert 0 < trigger_start, ValueError(trigger_start)
        
        tr_env = self.copy().envelop()
        tr_sta = tr_env.copy().running_average(width=sta, shift=True)
        tr_lta = tr_env.running_average(width=lta, shift=True)

        # trim both traces to same window
        starttime = max([tr_sta.starttime, tr_lta.starttime])
        endtime = min([tr_sta.endtime, tr_lta.endtime])
        for tr in [tr_sta, tr_lta]:
            tr.trim(starttime=starttime, endtime=endtime)
        
        # force sampling alignment by interpolating lta
        tr_lta.data = np.interp(tr_sta.rtime(), xp=tr_lta.rtime(), fp=tr_lta.data)
        tr_lta.starttime = tr_sta.starttime
        
        assert tr_sta.starttime == tr_lta.starttime
        assert tr_sta.delta == tr_lta.delta
        assert tr_sta.npts == tr_lta.npts

        tr_sta_over_lta = tr_lta.copy()
        tr_sta_over_lta.data = tr_sta.data / (tr_lta.data + 1.e-20)

        # I = tr_sta_over_lta.data >= trigger_start  # (tr_sta_over_lta.data.max() * trigger_start)
        # t_trigger_start = tr.atime()[I][0]
        
        return tr_sta, tr_lta, tr_sta_over_lta  # , t_trigger_start
        
    def _apply_filter(self, filter, zerophase):
        assert isinstance(self, Trace)
        self.data = filter(
            data=self.data,
            zerophase=zerophase,
            input_domain="time")
        return self

    def butterpass(self,
                   freqmin: Union[float, None] = None,
                   freqmax: Union[float, None] = None,
                   order: float = 4.,
                   zerophase: bool = True) -> None:
        """
        freqmin or freqmax can be None to switch easily between bandpass lowpass or highpass
        """
        if freqmin is None and freqmax is None:
            # means do nothing
            return self

        filter = ButterworthFilter(
            freqmin=freqmin, freqmax=freqmax,
            sampling_rate=1.0/self.delta, order=order)
        return self._apply_filter(filter=filter, zerophase=zerophase)

    def bandpass(self, freqmin: float, freqmax: float, order: float, zerophase: bool) -> None:
        return self.butterpass(freqmin=freqmin, freqmax=freqmax, order=order, zerophase=zerophase)

    def lowpass(self, freqmax: float, order: float, zerophase: bool) -> None:
        return self.butterpass(freqmin=None, freqmax=freqmax, order=order, zerophase=zerophase)

    def highpass(self, freqmin: float, order: float, zerophase: bool) -> None:
        return self.butterpass(freqmin=freqmin, freqmax=None, order=order, zerophase=zerophase)

    def gaussbandpass(self, freq0: float, alpha: float) -> None:
        assert freq0 > 0
        nfft = next_fast_len(self.npts)
        freq = fftfreq(nfft, self.delta)
        g = np.exp(-alpha * ((np.abs(freq) - freq0) / freq0) ** 2.0)

        self.data = ifft(g * fft(self.data, nfft)).real[:self.npts]
        return self

    def gaussbandstop(self, freq0: float, alpha: float) -> None:
        assert freq0 > 0
        nfft = next_fast_len(self.npts)
        freq = fftfreq(nfft, self.delta)
        g = np.exp(-alpha * ((np.abs(freq) - freq0) / freq0) ** 2.0)

        self.data -= ifft(g * fft(self.data, nfft)).real[:self.npts]
        return self

    def tzeros(self):
        """
        find the zeros of the trace by linear interpolation if it falls between two samples
        """
        tz = hyperzeros(t=self.rtime(), f=self.data, sign=0.0, assume_t_growing=True) + self.starttime
        return tz

    def tmax(self):
        return hypermax(t=self.rtime(), f=self.data) + self.starttime

    def envelop(self):
        self.data = np.abs(hilbert(self.data))
        return self

    def abs(self):
        self.data = np.abs(self.data)
        return self

    def oversamp_by_two(self):
        """
        pad the spectrum with zeros to oversamp the signal by a factor of two
        if the trace is a FFTTrace,
        if the trace is a Trace, their is one fft/ifft cycle applied
            use:
            tr.oversamp_by_two()
            or equivalently
            tr.fft().oversamp_by_two().ifft()

            nb: oversamp_by_two can be called many times like this
            tr.fft().oversamp_by_two().oversamp_by_two().oversamp_by_two().ifft()

        """
        # NB : the call below is not recursive because it calls
        # the oversamp_by_two method of FFTTrace not Trace
        return self.fft().oversamp_by_two().ifft()

    def decimate(self, decim_rate: int, anti_alias=0.95, anti_alias_order=4.0, anti_alias_zerophase=True):
        """
        more accurate than downsamp because the decimation rate is provided by the user.
        provides better control on the output sampling rate
        """
        assert decim_rate >= 2
        assert decim_rate % 1.0 == 0.

        current_nyquist = 0.5 / self.delta
        new_nyquist = 0.5 / (self.delta * decim_rate)

        if anti_alias:
            assert 0.0 <= anti_alias <= 1.0, anti_alias
            self.lowpass(anti_alias * new_nyquist,
                         order=anti_alias_order,
                         zerophase=anti_alias_zerophase)
        else:
            # I suppose you know what you are doing
            pass

        self.data = self.data[::decim_rate]
        self.delta *= decim_rate
        return self

    def downsamp(self, new_nyquist, anti_alias=0.95, anti_alias_order=4.0, anti_alias_zerophase=True):
        """
        the new nyquist frequency will not necessarilly be new_nyquist (might be a bit higher)
        """

        current_nyquist = 0.5 / self.delta
        
        if not new_nyquist < current_nyquist:
            raise ValueError(
                f"new_nyquist {new_nyquist} is not lower than "
                f"current_nyquist {current_nyquist}")

        if anti_alias:
            assert 0.0 <= anti_alias <= 1.0, anti_alias
            self.lowpass(anti_alias * new_nyquist,
                         order=anti_alias_order,
                         zerophase=anti_alias_zerophase)
        else:
            # I suppose you know what you are doing
            pass

        # if the decimation rate is not round, I floor it
        # => the output sampling might be a bit higher than the user may expect
        target_new_delta = 0.5 / new_nyquist
        decim_rate = int(np.floor(target_new_delta / self.delta))
        assert decim_rate >= 1
        self.data = self.data[::decim_rate]
        self.delta *= decim_rate  # not target_new_delta !
        if 0.5 / self.delta != new_nyquist:
            warnings.warn(f'new nyquist {new_nyquist} could not be reached, using {0.5 / self.delta} instead')

        return self

    def agc(self, width=0.1):
        """
        automatic gain control
        TODO: is there an "official" AGC algo?
        """
        # compute the envelope, smooth it in time
        env = self.copy().detrend().envelop().running_average(width=width, shift=False).data
        # normalize the envelop curve
        env = (env - env.min()) / (env.max() - env.min())

        self.data /= (0.9 * env + 0.1)
        return self

    def norm(self, mode="std"):
        if mode == "std":
            norm = self.data.std()

        elif mode == "i68":
            p16, p84 = np.percentile(self.data, [16, 84])
            norm = p84 - p16

        elif mode == "l1":
            norm = np.abs(self.data).sum()

        elif mode == "l2":
            norm = (np.abs(self.data) ** 2.).sum()

        elif mode == "max":
            norm = self.data.max()

        elif mode == "amax":
            norm = np.abs(self.data).max()

        elif mode == "energy":
            norm = self.energy()

        else:
            raise NotImplementedError(mode)

        if norm == 0.:
            pass  # do nothing

        elif norm > 0.:
            self.data /= norm

        elif np.isnan(norm):
            raise ValueError('norm is nan?', norm, self.data[:10], "...")

        elif np.isinf(norm):
            raise ValueError('norm is inf?', norm, self.data[:10], "...")

        else:
            raise ValueError('norm was negative?', norm)

        return self

    def integrate(self):

        self.data[1:] = 0.5 * (self.data[1:] + self.data[:-1]) * self.delta
        self.data[0] = 0 * self.data[1]
        self.data = self.data.cumsum()
        return self

    def derivate(self):
        self.data = np.gradient(self.data, edge_order=2)
        self.data /= self.delta
        return self

    def check_if_similar(self, other):
        """
        verify if self and other
        are similar enough for operations

        """
        if not self.__class__ == other.__class__:
            #TODO make sure it works for
            # Trace vs Trace and FFTTrace vs FFTTrace
            raise TypeError(f'types {type(self)} and {type(other)} are not similar')

        if self.starttime != other.starttime:
            raise StarttimeError(self.starttime, other.starttime)

        if self.npts != other.npts:
            raise NptsError(self.npts, other.npts)

        if self.delta != other.delta:
            raise SamplingRateError(self.delta, other.delta)

        # otherwise
        return True

    def __iadd__(self, other):
        """add the data of other to self if the two objects are considered similar"""
        self.check_if_similar(other)
        self.data += other.data
        return self

    def split_causal_acausal(self, change_causal_sign: bool):
        """
        separate the causal and acausal parts
        reverse the time of the acausal part

        self is the causal part !!

        eventually : œchange the sign of the causal part : no default on purpose
        :param change_causal_sign:
        :return:
        """
        if self.starttime < 0. < self.endtime:
            #n_negatives = np.searchsorted(self.atime(), 0., side="left")
            n_negatives = int(np.ceil(-self.starttime / self.delta))

        else:
            raise ValueError("time error", self.starttime, self.endtime)

        acausal_part = self.copy()
        acausal_part.data = acausal_part.data[:n_negatives+1][::-1]
        acausal_part.starttime += (n_negatives * acausal_part.delta)


        causal_part = self
        causal_part.data = causal_part.data[n_negatives:]  # include 0
        causal_part.starttime += n_negatives * causal_part.delta  # should be 0

        if change_causal_sign:
            causal_part.data *= causal_part.data.dtype.type(-1.)

        return causal_part, acausal_part

    def fold(self, change_causal_sign: bool):
        causal_part, acausal_part = \
            self.split_causal_acausal(change_causal_sign=change_causal_sign)

        dt = causal_part.delta
        if acausal_part.npts == causal_part.npts \
            and (acausal_part.starttime - causal_part.starttime) < dt / 1000.:

            causal_part.data += acausal_part.data
            causal_part.data /= 2.
        else:
            raise Exception('could not fold trace, because of unconsistent sampling')

        return causal_part


class DomainError(Exception):
    pass


class FFTTrace(Trace):

    def first_negative_frequency(self):
        return self.npts // 2 + self.npts % 2

    def frequencies(self):
        return fftfreq(self.npts, self.delta)

    def side(self, sign=1, zero=True, copy=False):
        freqs = self.frequencies()
        i_first_negative = self.first_negative_frequency()

        if sign > 0:
            if zero:
                f = freqs[:i_first_negative]
                d = self.data[:i_first_negative]
            else:
                f = freqs[1:i_first_negative]
                d = self.data[1:i_first_negative]
        elif sign < 0:
            f = freqs[i_first_negative:]
            d = self.data[i_first_negative, :]
        else:
            f = freqs
            d = self.data

        if copy:
            d = d.copy()

        return f, d

    def dominant_frequency(self):
        return dominant_frequency(fft_data=self.data, delta=self.delta)

    def energy(self):
        return fft_energy(fft_data=self.data, delta=self.delta)

    def show(self, ax: Union[None, plt.Axes]=None, *args, **kwargs):
        if ax is None:
            ax = plt.gca()
        f, d = self.side(sign=1, copy=False)
        return ax.plot(f, np.abs(d), *args, **kwargs)

    def to_trace(self):
        warnings.warn('FFTTrace.to_trace is obsolet, please use FFTTrace.ifft')
        return Trace(
            seedid=self.seedid,
            delta=self.delta,
            starttime=self.starttime,
            longitude=self.longitude,
            latitude=self.latitude,
            elevation=self.elevation,
            distance=self.distance,
            data=ifft(self.data).real)

    def ifft(self):
        """Cast a FFTTrace into Trace, call ifft, keep real part only"""
        if not isinstance(self, FFTTrace):
            raise TypeError('type is not FFTTrace')

        self.__class__ = Trace
        if len(self.data):
            self.data = ifft(self.data).real

        assert isinstance(self, Trace)
        assert not isinstance(self, FFTTrace)
        return self

    # ======================= PROCESSING
    def detrend(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def edge_detrend(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def taperwidth(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def trim(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def data_copy_between(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def shallow_copy_between(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def slide(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def running_average(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def stalta(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def _apply_filter(self, filter, zerophase):
        """overwrite the original method to run in fft domain"""
        assert isinstance(self, FFTTrace)
        self.data = filter(
            data=self.data,
            zerophase=zerophase,
            input_domain="fft")
        return self

    # bandpass in fourier domain handled (by _apply_filter)
    # lowpass in fourier domain handled (by _apply_filter)
    # highpass in fourier domain handled (by _apply_filter)

    def gaussbandpass(self, freq0, alpha):
        assert freq0 > 0
        freq = fftfreq(self.npts, self.delta)
        g = np.exp(-alpha * ((np.abs(freq) - freq0) / freq0) ** 2.0)
        self.data *= g
        return self

    def gaussbandstop(self, freq0, alpha):
        assert freq0 > 0
        freq = fftfreq(self.npts, self.delta)
        g = np.exp(-alpha * ((np.abs(freq) - freq0) / freq0) ** 2.0)
        self.data *= 1. - g
        return self

    def tzeros(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def tmax(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def envelop(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    # def abs(self, *args, **kwargs):
    #     raise DomainError("please return to time domain first")

    def oversamp_by_two(self):
        assert isinstance(self, FFTTrace)

        i_first_negative_freq = self.npts // 2 + self.npts % 2
        pos = self.data[:i_first_negative_freq]
        neg = self.data[i_first_negative_freq:]
        self.data = 2.0 * np.hstack((pos, np.zeros_like(pos), np.zeros_like(neg), neg))
        self.delta /= 2.0
        return self

    def decimate(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def downsamp(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def agc(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def norm(self, *args, **kwargs):
        raise DomainError("please return to time domain first")

    def integrate(self, *args, **kwargs):
        raise NotImplementedError

    def derivate(self, *args, **kwargs):
        raise NotImplementedError

    def psd(self, db=True, width_octave=0., resample_fraction_after_smooth=0.1, true_npts=None):

        # frequency sampling interval in Hz
        if true_npts is None:
            df = 1. / float(self.npts * self.delta)
        else:
            # if the data was padded with zeros, it is better to use the true number
            # of samples to get the right psd amplitudes
            df = 1. / float(true_npts * self.delta)

        fpsd, fft_data = self.side(sign=1, zero=False, copy=False)
        psd = (np.abs(fft_data * self.delta) ** 2.) * df

        if db:
            psd = 10. * np.log10(psd)

        if width_octave:
            med = psd.mean()
            psd = fsmooth1(fpsd, psd - med, width_octave=width_octave) + med

            if resample_fraction_after_smooth:
                dlog_freq = resample_fraction_after_smooth * width_octave * np.log(2.)

                log_freqs = np.log(fpsd)
                log_new_freqs = np.arange(log_freqs[0], log_freqs[-1], dlog_freq)

                psd = np.interp(log_new_freqs, xp=log_freqs, fp=psd)
                fpsd = np.exp(log_new_freqs)

        return fpsd, psd

    def whitening(self,
                  width_octave: float,
                  freqmin: float,
                  freqmax: float,
                  zerophase: bool = True,
                  order: int = 4,
                  water_level: float = 0.001) -> np.ndarray:

        self.data = spectral_whitening(
            fftdat=self.data,
            delta=self.delta,
            width_octave=width_octave,
            freqmin=freqmin,
            freqmax=freqmax,
            zerophase=zerophase,
            order=order,
            water_level=water_level)

        return self

    def power_whitening(self,
                  power: float,
                  freqmin: float,
                  freqmax: float,
                  zerophase: bool = True,
                  order: int = 4) -> np.ndarray:

        self.data = power_whitening(
            fftdat=self.data,
            delta=self.delta,
            power=power,
            freqmin=freqmin,
            freqmax=freqmax,
            zerophase=zerophase,
            order=order)

        return self


class FourierDomainTrace(FFTTrace):
    # obsolet
    pass


if __name__ == '__main__':

    data = np.zeros(12) * 0.0
    data[0] = 1.
    tr = Trace(data=data)
    print(tr, tr.__class__, tr.data)

    tr.fft()
    print(tr, tr.__class__, tr.data)

    tr.ifft()
    print(tr, tr.__class__, tr.data)
