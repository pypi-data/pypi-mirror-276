import numpy as np


def hyperzeros(t, f, sign=0., assume_t_growing=False):
    """find the zero crossing with subsample precision in 1d"""

    n = len(f)
    assert t.ndim == f.ndim == 1
    assert len(f) == len(t)
    if not assume_t_growing:
        assert np.all(t[1:] > t[:-1]), "t must be strctly growing"

    if f.min() > 0 or f.max() < 0.:
        return np.array([], dtype=f.dtype)

    D = f != 0.               # non null data
    J = D[1:] | D[:-1]        # avoid two zeros in a row, otherwhise there are nans below
    K = f[1:] * f[:-1] <= 0.  # sign change or one zero or two
    G = f[1:] >= f[:-1]       # growing or constant

    I = K & J  # sign change and at most one zero

    if sign > 0.:
        I &= G   # sign change, strictly growing

    elif sign < 0.:
        I = (K & J) & (~G)   # sign change, strictly decreasing

    i = np.arange(n-1)[I]

    tz = t[i+1] - f[i+1] * (t[i+1] - t[i]) / (f[i+1] - f[i])  # division ok thanks to J
    return tz


def isolate_sections_with_same_sign(t, f, assume_t_growing=False):
    """
    yields sub time and data array
    between the zero crossings
    use it to color positive an negative parts of a waveform
    """

    tz = hyperzeros(t, f, sign=0., assume_t_growing=assume_t_growing)  # does the assertions
    n = len(t)
    Ipos = f > 0
    if len(tz) == 0:
        if f[0] >= 0:
            yield 1, t, f

        elif f[0] < 0:
            yield -1, t, f

        else:
            raise Exception
    else:

        b = 0
        previous_tzero = t[0]
        for ttz in tz:
            e = np.searchsorted(a=t, v=ttz)

            tout = np.hstack((previous_tzero, t[b: e], ttz))
            fout = np.hstack((0., f[b: e], 0.))

            if Ipos[b:e].any():  # np.any(f[b: e] > 0):
                yield 1, tout, fout
            else:
                yield -1, tout, fout

            b = e
            previous_tzero = ttz
            if b == n:
                return

        tout = np.hstack((previous_tzero, t[b:], t[-1]))
        fout = np.hstack((0., f[b:], 0.))
        if Ipos[b:].any():  # np.any(f[b:] > 0):
            yield 1, tout, fout
        else:
            yield -1, tout, fout


def hypermax(t, f, axqc=None, assume_t_growing=False):
    """
    computes the max of f with sub-sample precision
    principle : interpolate locally the first derivatives and find the roots
    """
    if not assume_t_growing:
        assert (t[1:] > t[:-1]).all(), "t must be strictly growing"

    imax = np.argmax(f)
    tmax, fmax = t[imax], f[imax]
    
    if imax == 0:
        return t[0]

    elif imax == len(t) - 1:
        return t[-1]

    # old version
    # I = np.array([imax - 1, imax])
    # tmid = 0.5 * (t[1:] + t[:-1])
    # dfadt = (f[1:] - f[:-1]) / (t[1:] - t[:-1])
    # tt, ff = tmid[I], dfadt[I]
    # same faster
    tt = (0.5 * (t[imax: imax+2] + t[imax - 1: imax + 1]))
    ff = (f[imax: imax + 2] - f[imax - 1: imax + 1]) / (t[imax: imax + 2] - t[imax - 1: imax + 1])

    ip = np.argsort(ff)
    thypermax = np.interp(0., xp=ff[ip], fp=tt[ip])

    if axqc is not None:
        axqc.plot(t, f, "k+-", alpha = 0.4)
        axqc.plot(tmax, fmax, 'ko')
        # axqc.plot(dt, df, "r+-", alpha = 0.4)
        axqc.plot(tt, ff, "r", alpha = 1.0)
        axqc.plot(thypermax, 0, "r*", alpha = 1.0)
        axqc.plot(thypermax * np.ones(2), axqc.get_ylim(), 'r')
        axqc.grid(True)

    return thypermax


def hypermax_multi(t, f, assume_t_growing=False, axqc=None):
    """
    find all local maxima in f
    assumes that t is strictly growing

    """
    if not assume_t_growing:
        assert (t[1:] > t[:-1]).all(), "t must be strictly growing"

    tmid = 0.5 * (t[1:] + t[:-1])
    dfadt = (f[1:] - f[:-1]) / (t[1:] - t[:-1])

    thypermaxs = hyperzeros(tmid, dfadt, sign=-1, assume_t_growing=True)
    fmaxs = np.interp(thypermaxs, xp=t, fp=f)  # poor estimate of the local maximum amplitude

    if axqc is not None:
        axqc.plot(t, f, "k+-", alpha=0.4)
        # axqc.plot(tmaxs, fmaxs, 'ko')
        axqc.plot(tmid, dfadt, "r-", alpha=0.4)
        axqc.plot(thypermaxs, fmaxs, "m*", alpha=1.0)
        axqc.grid(True)

    return thypermaxs, fmaxs


def hypermin_multi(t, f, assume_t_growing=False):
    thypermins, fmins = hypermax_multi(t, -f, assume_t_growing=assume_t_growing, axqc=None)
    return thypermins, -fmins


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x = np.sort(np.random.randn(1000))
    y = np.random.randn(1000)
    # y[:10] = 0.
    y[110:200] = 0.
    # y[-10:] = 0.

    z = hyperzeros(x, y)
    plt.plot(x, y, 'k.-')
    for ss, tt, ff in isolate_sections_with_same_sign(x, y):
        if ss > 0:
            # plt.plot(tt, ff, 'b')
            plt.fill(tt, ff, 'b')
        elif ss < 0:
            # plt.plot(tt, ff, 'r')
            plt.fill(tt, ff, 'r')
        else:
            raise ValueError(ss)

    plt.plot(z, z * 0, 'ro')
    z = hyperzeros(x, y, sign=1)
    plt.plot(z, z * 0, 'wx')
    z = hyperzeros(x, y, sign=-1)
    plt.plot(z, z * 0, 'w+')
    ax = plt.gca()
    plt.figure()
    thypermaxs, ymaxs = hypermax_multi(x, y, axqc=plt.gca())


    ax.plot(thypermaxs, ymaxs, 'ms')
    plt.show()
