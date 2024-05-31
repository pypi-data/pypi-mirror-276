#!/usr/bin/env python
from typing import Union
import os
from copy import deepcopy
import warnings
import numpy as np
from tempoo.utc import UTCFromJulday
from seiscod.readwrite.rawtrace import RawTrace

try:
    # I DONT WANT ANYTHING FROM OBSPY IN THE DEFAULT IMPORTS !!!
    # DO NOT IMPORT ANYTHING FROM THIS FILE IN THE MAIN __INIT__ FILE
    from obspy import read as ocread
    from obspy.core import Stream as ObspyStream, AttribDict
    from obspy.core.compatibility import from_buffer

    from obspy.io.segy.segy import iread_segy
    from obspy.io.segy.segy import SEGYFile
    from obspy.io.segy.header import TRACE_HEADER_KEYS as SEGY_TRACE_HEADER_KEYS

    from obspy.io.seg2.seg2 import SEG2, SEG2InvalidFileError

except ImportError:
    raise Exception('obspy is required for these functions')


"""
31/08/21 : 
read segy data using obspy
Faster than obspy.read
because traces are not packed into obspy.core.trace.Trace objects 
(using obspy.io.segy.segy.SEGYFile is much faster)
NB: only for segy rev1

14/09/21 :
set trace to zero and re-export segy file

15/09
add SegyHeaderSelector

28/09 
replace SegyHeaderSelector and readsegy_using_obspy
by one single object SegyReaderUsingObspy for faster data reading

30/09/21
Separate segy and seg2
"""


class SegyReaderUsingObspy(object):

    def load(
            self,
            segyfile: str,
            segy_keys: Union[None, str, list, np.ndarray],
            endian=None,):
        """
        select the index of the traces based on one or more header fields
        the indexs can be provided then to readsegy_using_obspy

        :param segyfile: name of the file to read
        :param segy_keys: list of segy keys among obspy.io.segy.header.TRACE_HEADER_KEYS
        :return :
        """

        with open(segyfile, 'rb') as fid:
            segy_file_object = SEGYFile(
                file=fid,
                endian=endian,
                textual_header_encoding=None,
                unpack_headers=False,
                headonly=True,  # < leave to True even for headonly=False
                read_traces=True, # < leave to True even if only the headers are wanted
                )
            ntraces = len(segy_file_object.traces)

        segy_fields = {}
        if segy_keys is not None:

            if segy_keys == "*":
                # means all official segy keys
                segy_keys = SEGY_TRACE_HEADER_KEYS

            if not len(segy_keys) == len(np.unique(segy_keys)):
                raise ValueError("the segy_keys list is not unique")

            for index, segy_trace in enumerate(segy_file_object.traces):
                segy_trace_header = segy_file_object.traces[index].header

                for segy_key in segy_keys:
                    # __getattr__ means unpacking binary values,
                    # it slows the reading down if two many attributes are requested
                    segy_value = segy_trace_header.__getattr__(segy_key)

                    if index == 0:
                        segy_fields[segy_key] = [segy_value]

                    else:
                        segy_fields[segy_key].append(segy_value)

            for segy_key, list_of_values in segy_fields.items():
                segy_fields[segy_key] = np.asarray(list_of_values)
                assert len(segy_fields[segy_key]) == ntraces, (len(segy_fields[segy_key]), ntraces)

        self.segyfile = segyfile
        self.ntraces = ntraces
        self.segy_file_object = segy_file_object
        self.segy_fields = segy_fields

    def __init__(self,
                 segyfile: str,
                 segy_keys: Union[None, str, list, np.ndarray],
                 endian=None):
        """
        explore the trace headers and store the content internally
        use submethods to select trace indexs
        :param segyfile: name of hte file to read in
        :param segy_keys:
            list of trace header fields to unpack and store for trace selection (only)
            more keys can be unpacked later, no need to unpack everything now
        """

        self.segyfile = segyfile  # the name of the file read
        self.ntraces = 0          # the nimber of traces in the file
        self.segy_fields = {}     # the loaded header fields
        self.segy_file_object = None  # the raw trace list

        self.load(
            segyfile=segyfile, segy_keys=segy_keys, endian=endian)

    def select_trace_indexs_using_ranges(self,
        segy_keys: list,
        min_values: list,
        max_values: list) -> np.ndarray:
        """
        find trace indexs based on header fields
        select by ranges
        :param segy_keys: list of segy trace header fields to select on
        :param min_values: min value for each item of segy_keys
        :param max_values: max value for each item of segy_keys
        :retur trace_indexs: the indexs of the traces that fit in the selection
        """

        mask = np.ones(self.ntraces, dtype=bool)
        for segy_key, min_value, max_value in zip(segy_keys, min_values, max_values):
            segy_values = self.segy_fields[segy_key]
            mask &= (min_value <= segy_values) & (segy_values <= max_value)

        trace_indexs = np.arange(self.ntraces)[mask]
        return trace_indexs

    def select_trace_indexs_using_list_of_items_meshgrid(self,
        segy_keys: list,
        segy_lists: list) -> np.ndarray:
        """
        find trace indexs based on header fields
        select by specfic values

        :param segy_keys: list of segy trace header fields to select on
        :param segy_lists: list of list, the items to select for each field
        :retur trace_indexs: the indexs of the traces that fit in the selection
        """

        mask = np.ones(self.ntraces, dtype=bool)
        for segy_key, segy_values_requested_by_user in zip(segy_keys, segy_lists):

            segy_values_in_header = self.segy_fields[segy_key]
            mask &= np.in1d(ar1=segy_values_in_header, ar2=segy_values_requested_by_user)

        trace_indexs = np.arange(self.ntraces)[mask]
        return trace_indexs

    def select_trace_indexs_using_list_of_items_flat(self,
        segy_keys: list,
        segy_lists: list) -> np.ndarray:
        """
        find trace indexs based on header fields
        select by specfic values

        :param segy_keys: list of segy trace header fields to select on
        :param segy_lists: list of list, the items to select for each field
        :retur trace_indexs: the indexs of the traces that fit in the selection
        """
        for segy_list in segy_lists:
            assert len(segy_list) == len(segy_lists[0])

        mask = np.zeros(self.ntraces, dtype=bool)

        for tup in zip(*segy_lists):

            maski = np.ones(self.ntraces,dtype=bool)
            for segy_key, segy_value in zip(segy_keys,tup):
                segy_values_in_header = self.segy_fields[segy_key]
                maski &= segy_values_in_header == segy_value
            mask |= maski

        trace_indexs = np.arange(self.ntraces)[mask]
        return trace_indexs

    def unpack_traces(
            self, trace_indexs: Union[list, np.ndarray],
            segy_keys: Union[None, str, list, np.ndarray]=None,
            headonly: bool = False,
            copy: bool = True):
        """
        :param trace_indexs: the indexs of the traces to unpack from the SegyFile object
        :param segy_keys: the header values to unpack and which will be attached to the trace objects
        """
        allowed_segy_keys = SEGY_TRACE_HEADER_KEYS + ['starttime']

        raw_trace_list = []
        for trace_index in trace_indexs:
            segy_trace = self.segy_file_object.traces[trace_index]

            trace_dict = {
                "seedid": segy_trace.header.device_trace_identifier,
                "delta": segy_trace.header.sample_interval_in_ms_for_this_trace * 1e-6,
                "starttime": 0.}

            trace_data = None
            if not headonly:
                # put the data in the trace_dict
                trace_data = segy_trace.data

            if segy_keys is None:
                # attribute the values that are already unpacked from load
                for segy_key, values in self.segy_fields.items():
                    trace_dict[segy_key] = segy_trace.header.__getattr__(segy_key)

            elif segy_keys == "*":
                # means unpack all the fields from the trace headers
                segy_keys = SEGY_TRACE_HEADER_KEYS

                for segy_key in segy_keys:
                    trace_dict[segy_key] = segy_trace.header.__getattr__(segy_key)

            else:
                # user wants some segy keys that were not specified during the loading
                for segy_key in segy_keys:

                    if segy_key == "starttime":
                        # this is not a standard key
                        starttime = UTCFromJulday(
                            year=segy_trace.header.year_data_recorded,
                            julday=segy_trace.header.day_of_year,
                            hour=segy_trace.header.hour_of_day,
                            minute=segy_trace.header.minute_of_hour,
                            second=segy_trace.header.second_of_minute).timestamp
                        trace_dict['starttime'] = starttime

                    elif segy_key in allowed_segy_keys:
                        trace_dict[segy_key] = segy_trace.header.__getattr__(segy_key)

                    else:
                        raise KeyError(
                            f'segy_key {segy_key} not understood, '
                            f'the available keys are :\n'
                            + "\n".join(allowed_segy_keys))

            raw_trace = RawTrace(trace_dict=trace_dict, trace_data=trace_data)
            raw_trace_list.append(raw_trace)

        if copy:
            # make a copy so that modifications to stream_out
            # cannot impact the internal attributes of this object
            # and will have no impact on next call(s)
            raw_trace_list = [raw_trace.copy() for raw_trace in raw_trace_list]

        return raw_trace_list


def set_segy_traces_to_zero(
        segyfile_in: str,
        segyfile_out: str,
        trace_indexs: Union[list, np.ndarray]) -> None:
    """
    set all samples of some traces to 0
    all other header fields and data should be preserved
        including textual and binary headers, data encoding, endianess, revision, trace headers and order...

    :param segyfile_in: name of the segy file to read in (must exist)
    :param segyfile_out: name of the segy file to write out (must not exist)
    :param trace_indexs: indexs of the traces to replace by zeros
                         use segy_indexs_from_headers to determine the indexs
    """
    # TODO can be done using the new object SegyReaderUsingObspy

    if not os.path.isfile(segyfile_in):
        raise IOError(segyfile_in)

    if os.path.isfile(segyfile_out):
        raise IOError(f"{segyfile_out} exists already")

    trace_indexs = np.asarray(trace_indexs, int)
    if not len(trace_indexs):
        raise ValueError('trace_indexs is empty')

    with open(segyfile_in, 'rb') as fid:
        segy_file_object = SEGYFile(
            file=fid,
            endian=None,
            textual_header_encoding=None,
            unpack_headers=False,
            headonly=False,  # if True, the function works but the zeros are not writen
            read_traces=True)  # < leave to True
        ntraces = len(segy_file_object.traces)

        if not len(np.unique(trace_indexs)) == len(trace_indexs) <= ntraces:
            raise ValueError('trace indexs must be unique')

        if not (0 <= trace_indexs.min() < trace_indexs.max() <= ntraces-1).all():
            raise ValueError(f'traces indexs must be between 0 and {ntraces-1}')

        for trace_index in trace_indexs:
            zero = segy_file_object.traces[trace_index].data.dtype.type(0)
            segy_file_object.traces[trace_index].data[:] = zero

        segy_file_object.write(
            file=segyfile_out,
            data_encoding=segy_file_object.data_encoding,
            endian=segy_file_object.endian)

