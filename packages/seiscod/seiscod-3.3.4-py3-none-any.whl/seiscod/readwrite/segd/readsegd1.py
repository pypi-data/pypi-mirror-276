from typing import Union
import numpy as np
from seiscod.readwrite.rawtrace import RawTrace
from pysegd.segdfile import SegdFile
from tempoo.utc import UTCFromTimestamp

# instrument and orientation codes matching sensor types
# C. Satriano IPGP
_instrument_orientation_code = {
    0: '',  # not defined
    1: 'DH',  # hydrophone
    2: 'HZ',  # geophone, vertical
    3: 'H1',  # geophone, horizontal, in-line
    4: 'H2',  # geophone, horizontal, crossline
    5: 'H3',  # geophone, horizontal, other
    6: 'NZ',  # accelerometer, vertical
    7: 'N1',  # accelerometer, horizontal, in-line
    8: 'N2',  # accelerometer, horizontal, crossline
    9: 'N3'   # accelerometer, horizontal, other
}


# band codes matching sample rate, for a short-period instrument
# C. Satriano IPGP
def _band_code(sampling_rate):
    if sampling_rate >= 1000.:
        return 'G'
    if sampling_rate >= 250.:
        return 'D'
    if sampling_rate >= 80.:
        return 'E'
    if sampling_rate >= 10.:
        return 'S'


def read_segd(filename: str, headonly=False, indexs: Union[None, list, np.ndarray]=None):

    segdfile = SegdFile(filename)
    sample_interval_in_sec = segdfile.extended_header.sample_interval_in_microsec / 1e6
    number_of_samples_in_trace = segdfile.extended_header.number_of_samples_in_trace
    starttime = UTCFromTimestamp(segdfile.extended_header.gps_time_of_acquisition.timestamp())

    raw_trace_list = []  # Stream()

    for n_trace, trace in enumerate(segdfile.segd_traces):
        if indexs is not None and n_trace not in indexs:
            continue


        try:
            unit_serial_number = trace.trace_header.trace_header_external_blocks[6]['unit_serial_number']
            station = str(unit_serial_number)
        except (KeyError, IndexError):
            station = ""

        try:
            sensor_type = segdfile.extended_header.trace_header_external_blocks[1]['sensor_type']
            channel = _band_code(1. / sample_interval_in_sec) + _instrument_orientation_code[sensor_type]
        except (KeyError, IndexError):
            channel = ""

        trace_dict = {
            'npts': number_of_samples_in_trace,
            'seedid': f".{station}..{channel}",
            'delta': sample_interval_in_sec,
            'starttime': starttime,
            }

        if headonly:
            raw_trace = RawTrace(trace_dict=trace_dict, trace_data=np.array([]))

        else:
            # WARNING segdtrace.data_array is read only
            raw_trace = RawTrace(trace_dict=trace_dict, trace_data=trace.trace_data.data_array.copy())

        raw_trace_list.append(raw_trace)

    return raw_trace_list
