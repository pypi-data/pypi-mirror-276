import numpy as np
from scipy.fftpack import fftfreq


def smooth_irregular(x, y, width):
    """better use on detrend data !!!!"""
    assert len(x) == len(y)

    yy = np.zeros_like(y)
    yy[1:] = (.5 * (y[1:] + y[:-1]) * (x[1:] - x[:-1])).cumsum()  # trapeze integration
    xp = x + width / 2.
    xm = x - width / 2.
    yp = np.interp(xp, xp=x, fp=yy)
    ym = np.interp(xm, xp=x, fp=yy)
    w = (yp - ym) / (xp - xm)

    return w


def fsmooth1(freq, spectrum, width_octave=0.1):
    """
    smooth a spectrum array with logarithmically adaptive window

    :param freq: frequency array, sorted, unique, positive, growing, Hz
    :type freq: array
    :param spectrum: spectrum value, may be the spectrum itself (complex), or it's modulus (real)
        ** caution : the modulus of the averaged complex spectrum
                     is not the same as the average of the modulus of the spectrum
    :type spectrum: array
    :param width_octave: width of the smoothing window in octaves
        means that the running average window at frequency fi covers the range
               [fi * 2 ** (-.5 * width_octave), fi * 2 ** (+.5 * width_octave)]
            the window width is constant in logarithmic domain and is log(2) * width_octave
            i.e. [log(fi) -.5 * width_octave * log(2), log(fi) +.5 * width_octave * log(2)]
            where log is the natural logarithm
    :type width_octave: float
    :return fspectrum: smoothed version of sepctrum
    :rtype fspectrum: array (same dtype as spectrum)

    note : to use frequencies out of fft
    take
        freq = fftfreq(npts, delta)
        spectrum = fft(data)
        index_first_negative_freq = int(npts / 2 + npts % 2.)
        freqsup = freq[1:index_first_negative_freq]
        specsup = spectrum[1:index_first_negative_freq]

        -> call fsmooth1(freqsup, specsup, width_octave)

    """
    if not (freq > 0.).all():
        raise ValueError('frequency must be strictly positive')
    if not (freq[1:] > freq[:-1]).all():
        raise ValueError('frequency array must be growing')

    fspectrum = smooth_irregular(np.log(freq), spectrum, width=width_octave*np.log(2.))
    return fspectrum


def fsmooth1_negative(freq, spectrum, width_octave=0.1):
    """ same as fsmooth1 for negative frequency arrays

        freq = fftfreq(npts, delta)
        spectrum = fft(data)
        index_first_negative_freq = int(npts / 2 + npts % 2.)
        freqneg = freq[index_first_negative_freq:]
        specneg = spectrum[index_first_negative_freq:]

        -> call fsmooth1_negative(freqneg, specneg, width_octave)
    """

    return fsmooth1(-freq[::-1], spectrum[::-1], width_octave=width_octave)[::-1]


def fftsmooth(fftdat, delta, width_octave=0.1):
    """
    apply smoothing to data out of fft
    leave frequency 0 untouched !

    :param fftdat: fourier data to smooth, fft(data) (complex) or abs(fft(data)) (real)
    :type fftdat: array
    :param delta: sampling interval in s
    :param delta: s
    :param width_octave: width of the smoothing window in octaves
        means that the running average window at frequency fi covers the range
               [fi * 2 ** (-.5 * width_octave), fi * 2 ** (+.5 * width_octave)]
            the window width is constant in logarithmic domain and is log(2) * width_octave
            i.e. [log(fi) -.5 * width_octave * log(2), log(fi) +.5 * width_octave * log(2)]
            where log is the natural logarithm
    :type width_octave: float
    :return fftdat_smooth:
    """
    npts = len(fftdat)
    freq = fftfreq(npts, delta)
    i_first_negative_freq = int(npts / 2 + npts % 2.)

    # separate positive and negative sides of the spectrum
    freqsup = freq[1:i_first_negative_freq]  # freq[0] excluded
    freqinf = freq[i_first_negative_freq:]  # freq[0] excluded
    specsup = fftdat[1:i_first_negative_freq]
    specinf = fftdat[i_first_negative_freq:]

    # apply smoothing separately, ignore frequency 0
    specsup_smooth = fsmooth1(freqsup, specsup, width_octave=width_octave)
    specinf_smooth = fsmooth1_negative(freqinf, specinf, width_octave=width_octave)

    # merge results
    fftdat_smooth = np.zeros_like(fftdat)
    fftdat_smooth[1:i_first_negative_freq] = specsup_smooth
    fftdat_smooth[i_first_negative_freq:] = specinf_smooth

    return fftdat_smooth


if __name__ == '__main__':
    from scipy.fftpack import fft, ifft, fftfreq
    import matplotlib.pyplot as plt

    npts = 1024
    delta = 0.123
    t = np.arange(npts) * delta
    nu = fftfreq(npts, delta)

    data = np.random.randn(npts)
    data = ifft(fft(data) * np.exp(-2. * (abs(nu) / 0.5 - 1.0) ** 2.0)).real

    F = fft(data)

    # Smoothing complex data is the same as smoothing real and imaginary part separately
    G1 = fftsmooth(F, delta, width_octave=1.0)
    G2 = fftsmooth(F.real, delta, width_octave=1.0) + 1.j * fftsmooth(F.imag, delta, width_octave=1.0)
    assert (np.abs(G1 - G2) ** 2.0).mean() ** 0.5 < 1.e-10

    width_octave = 0.2
    # Warning : be careful with the modulus
    G1 = fftsmooth(abs(F), delta, width_octave=width_octave)
    G2 = abs(fftsmooth(F, delta, width_octave=width_octave))  # is different !

    # ========
    G = fftsmooth(abs(F), delta, width_octave=width_octave)

    plt.subplot(311)
    plt.plot(t, data)

    plt.subplot(312)
    plt.plot(nu, abs(F))
    plt.plot(nu, G)

    plt.subplot(313)
    plt.loglog(abs(nu), abs(F))
    plt.loglog(abs(nu), G)
    plt.show()
