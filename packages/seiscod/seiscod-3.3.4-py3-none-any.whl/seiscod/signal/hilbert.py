import numpy as np


def hconvertor(npts):
    """fourier domain conversion toward the analytical signal"""
    h = np.zeros(npts, dtype=float)
    if npts % 2 == 0:
        h[0] = h[npts // 2] = 1.0
        h[1:npts // 2] = 2.0
    else:
        h[0] = 1.0
        h[1:(npts + 1) // 2] = 2.0
    return h


if __name__ == '__main__':
    from scipy.signal import hilbert
    from scipy.fftpack import fft, ifft
    import matplotlib.pyplot as plt

    data = np.random.randn(256)  # must be real
    hdata1 = hilbert(data)
    hdata2 = ifft(fft(data) * hconvertor(len(data)))

    plt.plot(hdata1.real)
    plt.plot(hdata2.real, '--')
    plt.plot(hdata1.imag)
    plt.plot(hdata2.imag, '--')
    plt.show()

    data = np.random.randn(256) + 1.j * np.random.randn(256)
    hdata1 = fft(data) * hconvertor(len(data))
    hdata2 = fft(hilbert(data.real) + 1.j * hilbert(data.imag))

    plt.plot(hdata1.real)
    plt.plot(hdata2.real, '--')
    plt.plot(hdata1.imag)
    plt.plot(hdata2.imag, '--')
    plt.show()