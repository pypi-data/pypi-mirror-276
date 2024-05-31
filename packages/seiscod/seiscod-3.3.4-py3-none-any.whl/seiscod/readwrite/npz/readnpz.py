from typing import Union
import types
import numpy as np
from numpy.lib.npyio import _savez
from ..rawtrace import RawTrace


class NPZReader(object):
    def __init__(self, npzfilename: str):
        """
        :param self.npzfilename: file name to read
        """
        if not npzfilename.endswith('.seiscodstream.npz') and \
            not npzfilename.endswith('.seispystream.npz'):
            raise ValueError('npzfilename does not end with .seiscodstream.npz')
            

        self.npzfilename = npzfilename
        self.raw_trace_list = []

    def load_headers(self, additional_keys: Union[None, list, np.ndarray, str] = "*"):

        with np.load(self.npzfilename) as loader:
            delta = loader["delta"]
            starttime = loader["starttime"]
            seedid = loader["seedid"]
            longitude = loader["longitude"]
            latitude = loader["latitude"]
            elevation = loader["elevation"]
            distance = loader["distance"]

            if additional_keys is None:
                additional_keys = np.array([], str)

            elif "additional_keys" not in loader.files:
                # may be missing in file created before this version
                additional_keys = np.array([], str)

            else:
                available_additional_keys = loader["additional_keys"]

                if additional_keys == "*":
                    # load all available keys
                    additional_keys = available_additional_keys

                else:
                    # user provides a list of additional_keys to load
                    if not len(additional_keys) == len(np.unique(additional_keys)):
                        raise ValueError('additional_keys must be unique')

                    for key in additional_keys:
                        if key not in available_additional_keys:
                            raise KeyError(f"{key} not found in file, "
                                           f"available additional_keys are {available_additional_keys}")

            for array_id in range(len(delta)):
                data_key = 'data_{seedid}_{array_id}'.format(
                    seedid=seedid[array_id].replace('.', '_'),
                    array_id=array_id)

                trace_dict = {
                    "seedid": seedid[array_id],
                    "delta": delta[array_id],
                    "starttime": starttime[array_id],
                    "longitude": longitude[array_id],
                    "latitude": latitude[array_id],
                    "elevation": elevation[array_id],
                    "distance": distance[array_id],
                    # data not set here (leave to default for headonly)
                    "_data_key": data_key,
                    "_data_in": self.npzfilename}

                for key in additional_keys:
                    trace_dict[key] = loader[key][array_id]

                raw_trace = RawTrace(trace_dict=trace_dict, trace_data=None)
                self.raw_trace_list.append(raw_trace)
                #self.trace_dicts.append(trace_dict)

    def select(self, mask):
        assert len(mask) == len(self.raw_trace_list)
        self.raw_trace_list = [self.raw_trace_list[i] for i in range(len(mask)) if mask[i]]

    def load_data(self):
        """load the data for the traces found in self
        the user may have eliminated some traces based on the header
        """

        with np.load(self.npzfilename) as loader:
            for n, raw_trace in enumerate(self.raw_trace_list):
                if self.npzfilename != raw_trace.trace_dict['_data_in']:
                    raise ValueError('this is not the right npz file')
                raw_trace.trace_data = loader[raw_trace.trace_dict['_data_key']]

    def load(
            self, 
            headonly: bool=False,
            additional_keys: Union[None, list, np.ndarray, str] = None,
            trace_selector: Union[None, types.FunctionType] = None,
            trace_indexs: Union[None, list, slice] = None,
            ):
        """
        populate the object with a .seiscodstream.npz file

        :param headonly: If True, the data attributes of the traces will be left empty
        :param additional_keys:
            load the additional keys shared by all traces that have been saved in the file
            "*"  load all of them
            None load none of them
            ['key1', 'key2'] if you know which trace to load
        :param trace_selector:
            a function that is based on the header fields that returns True if the data must be loaded, False otherwhise
            example
                def trace_selector(trace: Trace) -> bool:
                    return "MYSTATION" in trace.seedid and trace.delta >= 0.001
        :return : nothing
            the traces loaded in self
        """

        self.load_headers(
            additional_keys=additional_keys)

        if trace_indexs is not None:
            mask = np.zeros(len(self.raw_trace_list), bool)
            mask[trace_indexs] = True
            self.select(mask)

        elif trace_selector is not None:
            # isolate some traces
            mask = np.array([trace_selector(raw_trace.trace_dict) for raw_trace in self.raw_trace_list], bool)
            self.select(mask)

        if not headonly:
            # load the data
            self.load_data()


def write_npz(seiscodstream, npzfilename: str, additional_keys: Union[None, str, list, np.ndarray] = "*"):
        """
        write the stream under npz format
        :param seiscodstream: a seiscod.stream.Stream object
        :param npzfilename: filename, must end with .seiscodstream.npz
        :param additional_keys: by default only a few attributes are saved in the npz file
            it is possible to save more attributes by mentionning their name in this list
            the attributes must exist in all traces (obtained using Stream.get)
        :return:
        """

        if not npzfilename.endswith('.seiscodstream.npz'):
            raise ValueError('npzfilename does not end with .seiscodstream.npz')

        if additional_keys is None:
            additional_keys = []

        elif additional_keys == "*":
            # assume all other traces have the same additionalkeys
            additional_keys = seiscodstream[0].additional_keys

        else:
            first_trace_additionalkeys = seiscodstream[0].additional_keys
            for key in additional_keys:
                if key not in first_trace_additionalkeys:
                    raise KeyError(
                        f"{key} not in the trace attributes, "
                        f"the available keys are: {first_trace_additionalkeys}")

        if not len(additional_keys) == len(np.unique(additional_keys)):
            raise Exception('additional_keys list must be unique')

        # == put the metadata into lists, one per item
        kwargs = {
            "npts":      np.asarray(seiscodstream.get('npts'), np.dtype('uint32')),
            "delta":     np.asarray(seiscodstream.get('delta'), np.dtype('float64')),
            "starttime": np.asarray(seiscodstream.get('starttime'), np.dtype('float64')),
            "seedid":    np.asarray(seiscodstream.get('seedid'), np.dtype('str')),
            "longitude": np.asarray(seiscodstream.get('longitude'), np.dtype('float64')),
            "latitude":  np.asarray(seiscodstream.get('latitude'), np.dtype('float64')),
            "elevation": np.asarray(seiscodstream.get('elevation'), np.dtype('float64')),
            "distance":  np.asarray(seiscodstream.get('distance'), np.dtype('float64')),
            "additional_keys": np.asarray(additional_keys, np.dtype('str'))}

        for key in kwargs['additional_keys']:
            if key in kwargs:
                raise ValueError(f'key "{key}" is saved by default and cannot be listed in the additional_keys')
            kwargs[key] = seiscodstream.get(key)  # let get raise if the key does not exist in all traces

        # == store the data arrays as individual items named
        #    data_network_station_location_channel_idnumber
        for array_id, trace in enumerate(seiscodstream):
            datakey = "data_{seedid}_{array_id}".format(
                seedid=trace.seedid.replace('.', '_'),
                array_id=array_id)
            kwargs[datakey] = trace.data
        try:
            _savez(npzfilename, args=(), compress=True, allow_pickle=False,
                   kwds=kwargs)
        except ValueError as e:
            if "Object arrays cannot be saved when allow_pickle=False" in str(e):
                for key, val in kwargs.items():
                    if not key.startswith("data_"):
                        print(key, val.__class__.__name__, val.dtype)
                for key, val in kwargs.items():
                    if str(val.dtype) == "object":
                        e.args = (str(e) + f"\n\tkey: '{key}' is a {val.__class__.__name__} with dtype={val.dtype}", )
            raise e

# def readseiscodstream(
#         npzfilename: str, headonly: bool=False,
#         additional_keys: Union[None, list, np.ndarray, str] = None,
#         trace_selector: Union[None, types.FunctionType]=None,
#         trace_indexs: Union[None, list] = None,
#         ) -> Stream:
#     """
#     read a seiscodstream saved under npz format
#     """
#     st = Stream()
#     st.from_npz(npzfilename=npzfilename, headonly=headonly,
#                 additional_keys=additional_keys,
#                 trace_selector=trace_selector,
#                 trace_indexs=trace_indexs,
#                 )
#     return st


