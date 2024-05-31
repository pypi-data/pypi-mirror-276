#!/usr/bin/env python
import sys, glob
import struct
import numpy as np
from ..rawtrace import RawTrace


SAMPLE_RATE_INDEX_HZ = {
    'GS V.3.00': {
        17: 500.e3,
        18: 1.e6,
        19: 2.e6,
        20: 2.5e6,
        21: 5e6,
        }}

GAIN = {
    'GS V.3.00': {
        0: 10.,
        1: 5.,
        2: 2.,
        3: 1.,
        4: 0.5,
        5: 0.2,
        6: 0.1
        }}


PROBE_MULTIPLIER = {
    'GS V.3.00': {
        0: 1.,
        1: 10.,
        2: 20.,
        3: 50.,
        4: 100.,
        5: 200.,
        6: 500.,
        7: 1000.,
        }}


COUPLING = {
    'GS V.3.00': {
        1: "DC",
        2: "AC"}}


def read_sig(filename: str, zero_at_trigger_time: bool = True):
    """
    :param filename:
    :return:
    """
    with open(filename, 'rb') as fid:
        file_version = fid.read(14).decode('ascii').replace('\x00', '')

        crlf1 = struct.unpack('h', fid.read(2))[0]

        channel_name = fid.read(9).decode('ascii').replace('\x00', '')

        crlf2 = struct.unpack('h', fid.read(2))[0]

        comment = fid.read(256).decode('ascii').replace('\x00', '')

        crlf3, control_z, sample_rate_index, operation_mode = \
            struct.unpack('4h', fid.read(4 * 2))

        trigger_depth = struct.unpack('i', fid.read(4))[0]

        trigger_slope, trigger_source, trigger_level = \
            struct.unpack('3h', fid.read(3 * 2))

        sample_depth = struct.unpack('i', fid.read(4))[0]

        captured_gain_index, captured_coupling_index = \
            struct.unpack('2h', fid.read(2*2))

        current_mem_ptr, starting_address, trigger_address, ending_address = \
            struct.unpack('4i', fid.read(4 * 4))

        trigger_time, trigger_date = \
            struct.unpack('2H', fid.read(2 * 2))  # uINT16 ????

        trigger_coupling_index, trigger_gain_index, \
            probe_multiplier_index, inverted_data = \
            struct.unpack('4h', fid.read(4*2))

        board_type = struct.unpack('1H', fid.read(2))[0]  # ???

        resolution_12_bits, multiple_record, trigger_probe, \
            sample_offset, sample_resolution, sample_bits = \
            struct.unpack('6h', fid.read(6 * 2))

        extended_trigger_time = struct.unpack('I', fid.read(4))[0]

        imped_a, imped_b = struct.unpack('2h', fid.read(2*2))

        external_tbs, external_clock_rate = \
            struct.unpack('2f', fid.read(2 * 4))

        file_options = struct.unpack('i', fid.read(4))[0]

        version = struct.unpack('H', fid.read(2))[0]

        eeprom_options, trigger_hardware, record_depth = \
            struct.unpack('3I', fid.read(3 * 4))

        padding = fid.read(127)  # 0 filled section to complete the 512 byte header
        assert fid.tell() == 512

        # ============================== INDEX TO VALUES
        try:
            probe_multiplier = PROBE_MULTIPLIER[file_version][probe_multiplier_index]
            captured_gain = GAIN[file_version][captured_gain_index]
            trigger_gain = GAIN[file_version][trigger_gain_index]
            sampling_rate = SAMPLE_RATE_INDEX_HZ[file_version][sample_rate_index]
            captured_coupling = COUPLING[file_version][captured_coupling_index]
            trigger_coupling = COUPLING[file_version][trigger_coupling_index]

        except KeyError:
            raise NotImplementedError(file_version, 
                probe_multiplier_index, 
                captured_gain_index, 
                sample_rate_index, 
                captured_coupling_index)

        # ============================== DATA SECTION
        # =========== check
        if probe_multiplier != 1:
            raise NotImplementedError(probe_multiplier)

        if inverted_data != 0:
            raise NotImplementedError(inverted_data)

        # =========== data type
        if resolution_12_bits == 0:
            # If the "resolution_12_bits" flag equals zero then the data is stored as unsigned 8 bit bytes.
            dtype = np.dtype('uint8')

        elif resolution_12_bits == 1:

            # if the "resolution_12_bits" flag equals one then the data is in the 12/16 bit format
            # which is stored as 16 bit signed integers (in the 12 bit mode the sampled data is sign extended
            # to 16 bits). For the 12 bit boards, the smallest value (-2047) represents –1V while the largest
            # value (+2047) represents +1V for the trigger level whereas the smallest and the largest values
            # represent +1V and –1V respectively for the captured data.
            dtype = np.dtype('int16')

        else:
            raise ValueError(resolution_12_bits)

        # =========== load data array
        if operation_mode == 2:
            # dual channel
            # The data is stored contiguously as a binary image of the saved
            # channel's signal storage space (one-half the memory depth).
            trace_data = np.fromfile(fid, count=sample_depth * dtype.itemsize, dtype=dtype)

        elif operation_mode == 1:
            # single channel
            # The data is interleaved as a binary image of the complete signal
            # storage space for the single channel mode (full memory depth).
            raise NotImplementedError(operation_mode)

        else:
            raise ValueError(operation_mode)

        # =========== unpack data array, type conversion
        if resolution_12_bits == 0:
            raise NotImplementedError

        elif resolution_12_bits == 1:
            assert probe_multiplier == 1.0  # I am unsure what to do otherwise
            trace_data = np.array(-1. * trace_data / captured_gain / 2047., np.dtype('float32'))

        if zero_at_trigger_time:
            starttime = -trigger_address / sampling_rate
        else:
            starttime = 0.

        # ========================= OUTPUT
        trace_dict = {
            "channel": channel_name,
            "npts": sample_depth,  # "sample_depth": sample_depth,
            "delta": 1. / sampling_rate,
            "starttime": starttime,
            "sig": {
                "file_version": file_version,
                "crlf1": crlf1,
                "name": channel_name,
                "crlf2": crlf2,
                "comment": comment,
                "crlf3": crlf3,
                "control_z": control_z,
                "sample_depth": sample_depth,
                "sample_rate_index": sample_rate_index,
                "operation_mode": operation_mode,
                "trigger_depth": trigger_depth,
                "trigger_slope": trigger_slope,
                "trigger_source": trigger_source,
                "trigger_level": trigger_level,
                "captured_gain_index": captured_gain_index,
                "captured_gain": captured_gain,
                "captured_coupling_index": captured_coupling_index,
                "captured_coupling": captured_coupling,
                "current_mem_ptr": current_mem_ptr,
                "starting_address": starting_address,
                "trigger_address": trigger_address,
                "ending_address": ending_address,
                "trigger_time": trigger_time,
                "trigger_date": trigger_date,
                "trigger_coupling_index": trigger_coupling_index,
                "trigger_coupling": trigger_coupling,
                "trigger_gain_index": trigger_gain_index,
                "trigger_gain": trigger_gain,
                "probe_multiplier_index": probe_multiplier_index,
                "probe_multiplier": probe_multiplier,
                "inverted_data": inverted_data,
                "board_type": board_type,
                "resolution_12_bits": resolution_12_bits,
                "multiple_record": multiple_record,
                "trigger_probe": trigger_probe,
                "sample_offset": sample_offset,
                "sample_resolution": sample_resolution,
                "sample_bits": sample_bits,
                "extended_trigger_time": extended_trigger_time,
                "imped_a": imped_a,
                "imped_b": imped_b,
                "external_tbs": external_tbs,
                "external_clock_rate": external_clock_rate,
                "file_options": file_options,
                "version": version,
                "eeprom_options": eeprom_options,
                "trigger_hardware": trigger_hardware,
                "record_depth": record_depth,
                }}

        raw_trace = RawTrace(trace_dict=trace_dict, trace_data=trace_data)
        return raw_trace


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    if "--test" in sys.argv[1:]:
        for item in sys.argv[1:]:
            if item == "--test":
                continue

            for filename in glob.iglob(item):
                try:
                    raw_trace = read_sig(filename)
                    print("V", filename, 'ok')
                except Exception as e:
                    print("X", filename, str(e).replace('\n', ' '))

    else:
        for filename in glob.iglob(sys.argv[1]):
            raw_trace = read_sig(filename)
            for k, v in raw_trace.trace_dict.items():
                print(k, v)

            plt.figure()
            plt.plot(raw_trace.trace_dict['starttime'] + np.arange(raw_trace.trace_dict['npts']) * raw_trace.trace_dict["delta"], raw_trace.trace_data)
            plt.show()
