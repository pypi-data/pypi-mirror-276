from typing import Union
import warnings
import numpy as np


"""
please do not remove assertions until the code is considered stable
"""


class TrimWindowError(Exception):
    pass


def pre_data_trim(
        current_starttime: float,
        delta: float,
        current_npts: int,
        required_starttime: Union[None, float],
        required_endtime: Union[None, float],
        accuracy: float = 1e-9):
    """
    prepare for data trimming, this function runs without data

    POLICY
        - Trimming is inclusive :
            if required_starttime falls at one sample, the sample is preserved
            same for required_endtime
            => knowing if a trim time equates a sample is a big source of bugs,
               so I introduce an accuracy parameter
        - ...
    """

    if not 0 < accuracy < delta:
        raise ValueError(accuracy)

    current_endtime = current_starttime + (current_npts - 1) * delta
    nb = ne = 0
    nbf = nef = 0.
    nbfr = nefr = 0.

    if required_starttime is not None:
        # user wants to act on starttime
        if required_starttime > current_endtime:
            # the trimming window starts after the last sample
            raise TrimWindowError(
                f"the required_starttime {required_starttime} "
                f"is after current_starttime {current_starttime}")

        # time difference between required and current starttime, positive: trim / negative: pad
        bdiff = required_starttime - current_starttime

        # convert to integer (not trivial)
        nbf = bdiff / delta  # floating number of samples to trim (if >0) or pad (if <0)
        nbfr = int(round(nbf))   # rounded number of samples, possibly 0

        # decide whether bdiff is considered as a round number of times the sampling
        # if np.abs(bdiff - nbfr * delta) < accuracy:
        if np.abs(nbf - nbfr) * delta < accuracy:
            # yes
            nb = nbfr  # possibly 0

            # if nb > 0: remove nb (>0) samples to the left of data
            #           v
            # x    x   [x    x   ...

            # if nb < 0:

        else:
            # no
            if bdiff > 0.0:
                # TRIMMING
                # remove nb (>0) samples to the left of data
                #              v
                # x    x    x  [ x   ...
                nb = int(np.floor(nbf)) + 1  # nbf = 2.6 => remove 3 samples
                # if nbf = 0.000000000000000000001 => nb = 1 > 0
                assert nb > 0, nb
            elif bdiff < 0.0:
                # PADING
                # padd with -nb zeros to the left side
                nb = int(np.ceil(nbf))  # nbf = -2.6 => nb = -2 => add 2 samples
                # if nbf = -0.000000000000000000001 => nb = 0 ==> add no samples
                assert nb <= 0, nb
            else:
                raise Exception('must not happen')

    if required_endtime is not None:
        if required_endtime < current_starttime:
            raise TrimWindowError(
                f"the required_endtime {required_endtime} "
                f"is before current_starttime {current_starttime}")

        ediff = current_endtime - required_endtime  # positive: trim / negative: pad
        nef = ediff / delta
        nefr = int(round(nef))

        # decide whether ediff is considered as a round number of times the sampling
        if np.abs(ediff - nefr * delta) < accuracy:
            # yes
            ne = nefr  # possibly 0
        else:
            # no
            if ediff > 0.0:
                # remove ne samples from the right hand side
                #        v
                #  ... x ]  x    x    x
                ne = int(np.floor(nef)) + 1  # nef = 2.6  => ne = 3 => remove ne samples
                assert ne > 0, ne

            elif ediff < 0.0:
                # add -ne samples to the right
                ne = int(np.ceil(nef))  # nef = -2.6 => ne = -2 => add two samples
                # assert ne > 0, (ne, nef)
                assert ne <= 0, (ne, nef, "???")  # modified from > to >= seems to work but correct???

            else:
                raise Exception('must not happen')

    if nb == ne == 0:
        return current_starttime, current_endtime, nb, ne

    assert nb + ne < current_npts, (nb, ne, current_npts)

    new_starttime = current_starttime + nb * delta  # possibly nb == 0
    new_endtime = new_starttime + (current_npts - nb - ne - 1) * delta

    if required_starttime is not None:
        if not np.abs(nb - nbf) * delta <= delta - accuracy:
            # if not np.abs(new_starttime - required_starttime) <= delta - accuracy:
            """
            new_starttime - required_starttime
                   = current_starttime + nb * delta - required_starttime
                   = current_starttime - required_starttime + nb * delta
                   = -bdiff + nb * delta
                   = (-bdiff / delta + nb) * delta
                   = (-nbf + nb) * delta
                   = (nb - nbf) * delta
            the test above is equivalent to testing that
                the delay between asked time and actual one is less than delta - accuracy
                but the following syntax is fucking not accurate enough
                "if not np.abs(new_starttime - required_starttime) <= delta - accuracy:"
            """

            msg = f"""
                current_starttime:  {current_starttime:+.16f} 
                required_starttime: {required_starttime:+.16f}
                new_starttime:      {new_starttime:+.16f}
                req-new:            {required_starttime - new_starttime:+.16f}         
                delta:              {delta:+.16f}
                accuracy:           {accuracy:+.16f}
                nbf:{nbf} nbfr:{nbfr} nb:{nb}
                
                delta - accuracy:                           {delta - accuracy:+.16f}         
                np.abs(nb- nbf) * delta:                    {np.abs(nb- nbf) * delta:+.16f}
                np.abs(new_starttime - required_starttime): {np.abs(new_starttime - required_starttime):+.16f}
                np.abs(nb- nbf) * delta  <= delta - accuracy:                   {np.abs(nb- nbf) * delta <= delta - accuracy}
                np.abs(new_starttime - required_starttime) <= delta - accuracy: {np.abs(new_starttime - required_starttime) <= delta - accuracy} 
                """
            print(msg)

            import matplotlib.pyplot as plt
            plt.figure()
            plt.plot(np.arange(current_npts),
                     current_starttime + np.arange(current_npts) * delta, 'k+')
            plt.plot([0, current_npts], [required_starttime, required_starttime], 'r-', label="required_starttime")
            plt.plot([0, current_npts], [new_starttime, new_starttime], 'bx--', label="new_starttime")
            plt.gca().legend()
            plt.show()

            raise ValueError(msg)

    if required_endtime is not None:
        if not np.abs(nef - ne) * delta < delta - accuracy:
            # if not np.abs(new_endtime - required_endtime) < delta - accuracy:

            """
            new_endtime - required_endtime
                = new_starttime + (current_npts - nb - ne - 1) * delta - required_endtime 
                = current_starttime + nb * delta + (current_npts - nb - ne - 1) * delta - required_endtime
                = current_starttime - required_endtime + (current_npts - 1) * delta - ne * delta
                = current_starttime + (current_npts - 1) * delta - required_endtime - ne * delta
                = current_endtime - required_endtime - ne * delta
                = ediff - ne * delta
                = (nef - ne) * delta
            so
                np.abs(nef - ne) * delta < delta - accuracy 
            is equivalent to 
                np.abs(new_endtime - required_endtime) < delta - accuracy
            but more accurate
            """
            msg = f"""
                current_starttime:  {current_starttime:.16f} 
                required_endtime:   {required_endtime:.16f}
                new_endtime:        {new_endtime:.16f}
                req-new:            {required_endtime - new_endtime:.16f}         
                delta:              {delta:.16f}
                accuracy:           {accuracy:.16f}
                """
            print(msg)

            import matplotlib.pyplot as plt
            plt.figure()
            plt.plot(current_starttime + np.arange(current_npts) * delta,
                     current_starttime + np.arange(current_npts) * delta, 'k+')
            plt.plot(required_endtime, required_endtime, 'rx')
            plt.plot(new_endtime, new_endtime, 'bx')
            plt.show()

            raise ValueError(msg)

    return new_starttime, new_endtime, nb, ne


# def data_trim(current_starttime: float,
#         delta: float,
#         data: np.ndarray,
#         required_starttime: Union[None, float],
#         required_endtime: Union[None, float],
#         fill_value: float = 0.,
#         accuracy: float = 1e-9):
#     """
#     warning : if the timewindow is shorter or equal to the original one, the data returned is a shallow copy of the data
#     if padding is involved, the returned data is a deep copy
#     """
#
#     current_npts = len(data)
#
#     new_starttime, new_endtime, nb, ne = pre_data_trim(
#         current_starttime=current_starttime,
#         delta=delta,
#         current_npts=current_npts,
#         required_starttime=required_starttime,
#         required_endtime=required_endtime,
#         accuracy=accuracy)
#
#     if ne > 0:
#         data = data[:-ne]  # not a copy by default
#     elif ne < 0:
#         data = np.hstack((data, fill_value * np.ones(-ne, dtype=data.dtype)))  # copy
#     else:
#         pass
#
#     if nb > 0:
#         data = data[nb:]   # not a copy by default
#     elif nb < 0:
#         data = np.hstack((fill_value * np.ones(-nb, dtype=data.dtype), data))  # copy
#     else:
#         pass
#
#     assert len(data) == current_npts - nb - ne
#
#     return new_starttime, data


def trim_data(current_starttime: float,
                      delta: float,
                      data: np.ndarray,
                      required_starttime: Union[None, float],
                      required_endtime: Union[None, float],
                      fill_value: float = 0.,
                      accuracy: float = 1e-9,
                      copy: bool=True):
    """
    """

    current_npts = len(data)

    new_starttime, new_endtime, nb, ne = pre_data_trim(
        current_starttime=current_starttime,
        delta=delta,
        current_npts=current_npts,
        required_starttime=required_starttime,
        required_endtime=required_endtime,
        accuracy=accuracy)

    if nb == 0 and ne == 0:
        if copy:
            data = data.copy()
        return current_starttime, data

    elif ne > 0:
        if nb > 0:
            data = data[nb:-ne]  # shallow copy
            if copy:
                data = data.copy()
            return new_starttime, data

        elif nb == 0:
            data = data[:-ne]
            if copy:
                data = data.copy()
            return new_starttime, data

        else:  # if nb < 0:
            startpad = fill_value * np.ones(-nb, dtype=data.dtype)
            if not copy:
                warnings.warn('copy implicitly requested by the triming window')
            newdata = np.hstack((startpad, data[:-ne]))  # the copy is implicit here...
            return new_starttime, newdata

    elif ne == 0:
        if nb > 0:
            data = data[nb:]  # shallow copy
            if copy:
                data = data.copy()
            return new_starttime, data

        elif nb < 0:
            startpad = fill_value * np.ones(-nb, dtype=data.dtype)
            newdata = np.hstack((startpad, data))  # hstack implies copy
            if not copy:
                warnings.warn('copy implicitly requested by the triming window')
            return new_starttime, newdata

        else:  # nb == 0
            raise Exception('handled before')

    else:  # if ne < 0:
        if not copy:
            warnings.warn('copy implicitly requested by the triming window')

        endpad = fill_value * np.ones(-ne, dtype=data.dtype)

        if nb > 0:
            newdata = np.hstack((data[nb:], endpad))  # copy implied
            return new_starttime, newdata

        elif nb == 0:
            newdata = np.hstack((data, endpad))  # copy implied
            return new_starttime, newdata

        else:  # if nb < 0:
            startpad = fill_value * np.ones(-nb, dtype=data.dtype)
            newdata = np.hstack((startpad, data, endpad))  # copy implied
            return new_starttime, newdata
