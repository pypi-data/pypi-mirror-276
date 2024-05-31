#!/usr/bin/env python


if __name__ == '__main__':
    from obspy.io.segy.segy import TRACE_HEADER_KEYS

    for key in TRACE_HEADER_KEYS:
        print(key)
