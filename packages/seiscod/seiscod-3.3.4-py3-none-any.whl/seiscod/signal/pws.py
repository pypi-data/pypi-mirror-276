import numpy as np
from scipy.signal import hilbert


def pws(datas, pg=1.0, norm_weighting_function=False):
    """
    Compute the phase weighted stack of a 2D array along axis 0
    source : Rost and Thomas 2002
    :param datas: 2D array, with real time domain data
    :param pg: float, strength of the weighting, 0.0 corresponds to non weighted stack (i.e. mean)
    :return: d, 1D array stacked along axis 0
    """

    analytical_signal = hilbert(datas, axis=1)
    instantaneous_phase = np.angle(analytical_signal)
    weighting_function = np.abs(np.mean(np.exp(1.j * instantaneous_phase), axis=0))
    if norm_weighting_function:
        weighting_function = weighting_function / weighting_function.max()

    return np.mean(datas, axis=0) * (weighting_function ** pg)

