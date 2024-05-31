import numpy as np
from scipy.fftpack import fftfreq


def dominant_frequencies(fft_datas: np.ndarray, delta: float) -> np.ndarray:
    """compute dominant frequency of an array from fft,
    using the average of positive frequencies weighted by the square modulus of the signal
    """

    nsta, nfft = fft_datas.shape
    i_first_negative_freq = nfft // 2 + nfft % 2
    freqs = fftfreq(nfft, delta)[1:i_first_negative_freq]

    square_modulus = abs(fft_datas[:, 1:i_first_negative_freq]) ** 2.
    I_0 = square_modulus.sum(axis=1) == 0

    dominant_frequency_array = np.zeros(nsta, float)

    dominant_frequency_array[~I_0] = \
        (freqs * square_modulus[~I_0, :]).sum(axis=1) / \
        square_modulus[~I_0, :].sum(axis=1)

    dominant_frequency_array[I_0] = 1.e-20
    dominant_frequency_array = dominant_frequency_array.clip(1e-20, np.inf)

    if np.isnan(dominant_frequency_array).any():
        raise ValueError

    if np.isinf(dominant_frequency_array).any():
        raise ValueError

    return dominant_frequency_array


def dominant_frequency(fft_data: np.ndarray, delta: float) -> float:
    return dominant_frequencies(fft_datas=fft_data[np.newaxis, :], delta=delta)[0]
