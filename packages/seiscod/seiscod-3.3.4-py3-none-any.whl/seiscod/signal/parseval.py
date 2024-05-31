from typing import Union
import numpy as np

"""
simply to remember parseval relation for discrete signals

the energy of a discrete time signal is (rectangle integration) 

Et = np.sum(np.abs(x) ** 2. * dt)
    where x is the time domain array
    dt is the sampling interval, s
    
    => Et is in [x] ** 2 * [s]
    
in frequency 

Ef = np.sum(np.abs(fft(x) * dt) ** 2.) * df
    where x is the time domain array
    dt is the sampling interval, s
    df is the frequency interval, Hz, df = 1 / (npts * dt)
    
    => Ef is in [x] ** 2 * [s] => consistent with Et
    
why fft(x) * dt and not simply fft(x)?
    the discretization of the signal using the Shah distribution 
    implies a distortion of the fourier amplitudes
    that must be corrected

    said differently :
      the true Fourier transform implies a unit change 
        TF[f](nu) = integral(f(t) * exp(2i pi nu t) dt) 
        => unit in [f] * [s]
      but the fft do not imply any unit change (from this source https://scipy.github.io/devdocs/tutorial/fft.html)
        fft[f]_k = sum_{n=0}^{N-1}{f_n * exp(-2i pi * k * n / N)} 
        => unit in [f]
      the multiplication by dt accounts for this difference 


For psd computations : 
    what seismologists usually mean by psd is 
    PSD_k = 2 * |dt * fft[f]_k|^2 / (npts * dt)
        where 
            f in [m]/[s]^2
            fft[f]_k in [m]/[s]^2
            dt * fft[f]_k in [m]/[s]
            |dt * fft[f]_k|^2 in [m]^2/[s]^2
            |dt * fft[f]_k|^2 / (npts * dt) in [m]^2/[s]^3
            => in [m]^2/[s]^4*[s]
            => in [m]^2/[s]^4/[Hz]
    NB1 : PSD_k must be multiplied by 2 to account for negative freqs
    NB2 : tapers decrease the power of the signal and can be corrected, see McNamara 2004
    
"""


def time_energy(time_data: np.ndarray, delta: float, axis: int = -1) -> Union[float, np.ndarray]:
    """
    :param time_data: time series 
    :param delta: 
    :return: 
    """
    # assert time_data.ndim == 1
    energy = (np.abs(time_data) ** 2. * delta).sum(axis=axis)
    return energy


def fft_energy(fft_data: np.ndarray, delta: float, axis: int = -1) -> Union[float, np.ndarray]:
    """
    :param fft_data: must directly result from scipy.fftpack.fft
    :param delta:
    :return:
    """
    # assert fft_data.ndim == 1
    npts = fft_data.shape[axis]
    df = 1. / float(npts * delta)

    energy = ((np.abs(fft_data * delta) ** 2.) * df).sum(axis=axis)
    return energy


if __name__ == '__main__':
    from scipy.fftpack import fft
    data = np.random.randn(3, 1024)
    delta = 0.123456

    fft_data = fft(data, axis=-1)

    et = time_energy(data, delta)
    ef = fft_energy(fft_data, delta, axis=-1)
    ef1 = fft_energy(abs(fft_data), delta, axis=-1)  # is the same
    err = np.abs(et - ef) / et
    print(et)
    print(ef)
    print(err)
    assert np.all(err < 1.e-12)
