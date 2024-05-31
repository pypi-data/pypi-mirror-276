import numpy as np


def cos_taper_four_points(starttime: float, npts: int, sampling_rate: float, t0: float, t1: float, t2: float, t3: float):
    assert t0 < t1 < t2 < t3
    delta = 1. / sampling_rate
    t = starttime + np.arange(npts) * delta
    i0, i1, i2, i3 = np.searchsorted(t[1:] - .5 / sampling_rate, [t0, t1, t2, t3])

    fupward = lambda x: (1. - np.cos(np.pi * (x - t0) / (t1 - t0))) / 2.0  # between t0 and t1
    fdownward = lambda x: (1. + np.cos(np.pi * (x - t2) / (t3 - t2))) / 2.0  # between t2 and t3

    tap = np.concatenate(
        (np.zeros(i0),
         fupward(t[i0:i1]),
         np.ones(i2 - i1),
         fdownward(t[i2:i3]),
         np.zeros(npts-i3)))
    return tap


def cos_taper_width(npts, sampling_rate, width, dtype=float, left=True, right=True):
    """
    time domain cosine taper

    :param npts: number of samples
    :param sampling_rate: sampling rate in Hz
    :param width: width of the cosine taper, in sec
    :return tap: taper array
    """
    assert left or right
    tap = np.ones(npts, dtype)
    nwidth = int(round(width * sampling_rate)) + 1  # excluded
    if not nwidth:
        return tap

    t = np.arange(npts) / sampling_rate
    T = 2. * width
    ttap = 1. - (np.cos(2. * np.pi * t[:nwidth] / T) + 1.) * .5
    if left:
        tap[:nwidth] = ttap  # ttap[::-1]
    if right:
        tap[-nwidth:] = ttap[::-1]
    return tap
