#!/usr/bin/env python
import sys
from seiscod.readwrite.segy.readsegyusingobspy \
    import SegyReaderUsingObspy, SEGY_TRACE_HEADER_KEYS
import numpy as np


def segy_trace_headers_to_csv(segyfilename: str):
    segy_reader = SegyReaderUsingObspy(segyfile=segyfilename, segy_keys=None)
    trace_indexs = np.arange(segy_reader.ntraces)
    trace_dicts = segy_reader.unpack_traces(
        trace_indexs=trace_indexs, segy_keys='*', headonly=True)

    header = "#" + ",".join(SEGY_TRACE_HEADER_KEYS)
    csv_rows = [header]
    for trace_dict in trace_dicts:
        csv_row = ",".join([str(trace_dict[key]) for key in SEGY_TRACE_HEADER_KEYS])
        csv_rows.append(csv_row)
    return '\n'.join(csv_rows)


if __name__ == '__main__':
    print(segy_trace_headers_to_csv(sys.argv[1]))
