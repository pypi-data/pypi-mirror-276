"""
TODO to be upgraded or removed
"""


if __name__ == '__main__':
    import sys, time
    import matplotlib.pyplot as plt
    import platform

    OPERATING_SYSTEM = platform.system().upper()

    help = """
    -h : print help and return
    -l : list segy keys and return
    -f : segyfile to read in
    -1 : first key, used to form gathers
    -2 : secondary key, used to sort the traces in the gather
    -s1 : select range of values for first key
    -s2 : select range of values for second key 
    -bp : filter between fmin and fmax Hz
    -t : trim 
    -nstd : normalize the traces by there std
    """
    argv = sys.argv[1:]
    if "-h" in argv or len(argv) == 0:
        print(help)
        sys.exit(0)

    if "-l" in argv:
        print("\n".join(SEGY_TRACE_HEADER_KEYS))
        sys.exit(0)

    if "-f" in argv:
        for narg, arg in enumerate(argv):
            if arg == "-f":
                break
        segyfile = argv[narg+1]
        assert os.path.isfile(segyfile), IOError(segyfile)
    else:
        raise Exception('-f option required')

    if "-1" in argv:
        for narg, arg in enumerate(argv):
            if arg == "-1":
                break
        first_segy_key = argv[narg+1]
        assert first_segy_key in SEGY_TRACE_HEADER_KEYS
    else:
        raise Exception('-1 option required')

    if "-2" in argv:
        for narg, arg in enumerate(argv):
            if arg == "-2":
                break
        second_segy_key = argv[narg+1]
        assert second_segy_key in SEGY_TRACE_HEADER_KEYS
    else:
        raise Exception('-2 option required')

    if "-s1" in argv:
        for narg, arg in enumerate(argv):
            if arg == "-s1":
                break

        first_segy_key_min_value = float(argv[narg + 1])
        first_segy_key_max_value = float(argv[narg + 2])

    else:
        first_segy_key_min_value = -np.inf
        first_segy_key_max_value = np.inf

    if "-s2" in argv:
        for narg, arg in enumerate(argv):
            if arg == "-s2":
                break

        second_segy_key_min_value = float(argv[narg + 1])
        second_segy_key_max_value = float(argv[narg + 2])

    else:
        second_segy_key_min_value = -np.inf
        second_segy_key_max_value = np.inf

    # =================================
    if "-t" in argv:
        for narg, arg in enumerate(argv):
            if arg == "-t":
                break

        trim_start = float(argv[narg + 1])
        trim_end = float(argv[narg + 2])

    else:
        trim_start = None
        trim_end = None

    if "-bp" in argv:
        for narg, arg in enumerate(argv):
            if arg == "-bp":
                break

        bandpass_fmin = float(argv[narg + 1])
        bandpass_fmax = float(argv[narg + 2])

    else:
        bandpass_fmin = None
        bandpass_fmax = None

    normalize_by_std = "-nstd" in argv

    # =================================
    sr = SegyReaderUsingObspy(
        segyfile,
        segy_keys=[first_segy_key, second_segy_key])

    values_of_first_segy_key = \
        np.unique(sr.segy_fields[first_segy_key])
    print(f'The values for {first_segy_key} are :')
    print(values_of_first_segy_key)

    values_of_first_segy_key = \
        values_of_first_segy_key[
            (values_of_first_segy_key >= first_segy_key_min_value) &
            (values_of_first_segy_key <= first_segy_key_max_value)
            ]

    if not len(values_of_first_segy_key):
        raise ValueError(
            f'no data for {first_segy_key}'
            f' between {first_segy_key_min_value} and {first_segy_key_max_value}')
    print(f'The selected values for {first_segy_key} are :')
    print(values_of_first_segy_key)

    for value_of_the_first_key in values_of_first_segy_key:
        trace_indexs = sr.select_trace_indexs_using_ranges(
            segy_keys=[first_segy_key, second_segy_key],
            min_values=[value_of_the_first_key, second_segy_key_min_value],
            max_values=[value_of_the_first_key, second_segy_key_max_value])

        if not len(trace_indexs):
            raise ValueError(
                f'no data for {first_segy_key}'
                f' between {first_segy_key_min_value} and {first_segy_key_max_value}'
                f' and {second_segy_key}'
                f' between {second_segy_key_min_value} and {second_segy_key_max_value}')

        raise NotImplementedError('TODO : update the output signature of sr.unpack_traces')
        stream = sr.unpack_traces(
            trace_indexs=trace_indexs,
            segy_keys=None)
        stream.sort_by(second_segy_key)
        # ======== process
        if trim_start is not None:
            for trace in stream:
                trace.trim(trim_start, trim_end)

        if bandpass_fmin is not None:
            for trace in stream:
                trace.bandpass(bandpass_fmin, bandpass_fmax, 4., True)

        if normalize_by_std:
            for trace in stream:
                trace.norm('std')

        stream.shade(
            ax=plt.gca(),
            timeticks=False,
            swapxy=True,
            powergain=0.4,
            ydim=second_segy_key)
        plt.gca().set_xlabel(second_segy_key)
        plt.gca().set_title(f'{first_segy_key}: {value_of_the_first_key}')
        plt.gcf().suptitle(segyfile)

        if OPERATING_SYSTEM == "LINUX":
            # on linux show the current figure
            # in interactive mode on,
            # this will preserve the same figure
            # all along the loop,
            # "input" freezes the figure on Windows
            plt.ion()
            plt.show()
            input('pause : press enter to move to the next gather')
            plt.gcf().clf()

        else:
            # more stable on windows
            # implies closing and re openeing the window every time
            print('press q on the figure (or close it) to move to the next gather')
            plt.ioff()
            plt.show()
            plt.close(plt.gcf())

