from typing import Union
import warnings
import numpy as np
from scipy.fftpack import fft, ifft, fftfreq, next_fast_len
import scipy.sparse as sp
from scipy.sparse import linalg as splinalg
from seiscod.signal.hypermax import hypermax, hypermax_multi, hypermin_multi
import matplotlib.pyplot as plt
import numexpr as ne


def exp(x: np.ndarray) -> np.ndarray:
    """
    significantly faster than numpy
    https://stackoverflow.com/questions/44190128/why-is-numpys-exp-slower-than-matlab-how-to-make-it-faster
    """
    return ne.evaluate('exp(x)')


def ccf_trim(nlag: int, nfft: int, centered: bool) -> np.ndarray:
    """
    get indexs to extract npad samples each side of the zero after fft_correlate

    apply the index array to ccf_lagtime and ifft(ccf_array) from fft_correlate
    to get a symertric lag array centered on 0 (odd number of samples)

    """
    if (2 * nlag + 1) > nfft:
        warnings.warn(f'cannot extract more than nlag={nfft // 2 - 1} if nfft={nfft}, got nlag={nlag}')
        nlag = nfft // 2 - 1

    if centered:
        b = nfft // 2 - nlag  # first sample preserved, included
        e = b + (2 * nlag + 1)  # first sample excluded
        return np.arange(b, e)

    else:
        p = np.arange(nlag + 1)  # first npad samples including 0
        n = np.arange(nfft - nlag, nfft)  # last npad samples
        return np.hstack((p, n))


# from proton.timer import Timer
def fft_correlate_many(
        fft_datas_ref: np.ndarray,
        fft_datas: np.ndarray,
        delta: float,
        t0_datas_ref: Union[float, np.ndarray] = 0.,
        t0_datas: Union[float, np.ndarray] = 0.,
        norm: bool = False,
        centered: bool = True,
        derivate: bool = False):
    """
    NB1 : positive lag time means that data is shifted to the right relative to data_ref
    NB2 : the data must be zero padded before fft (not done here)
          the ccf lateral parts are safe up to npad samples each side of the zero
          after that time folding may affect the reliability of the correlation function
          the number of samples used to pad the data have no impact
          on the ccf amplitude even when norm is True (TODO : test that)

    :param fft_datas_ref: 1d or 2d array, the fft of the reference waveform(s)
    :param fft_datas: 2d array, the fft of all the waveforms to correlate with the reference
    :param delta: sampling interval in s, same for all waveforms
    :param t0_datas_ref: starttime of the reference wavefrom in s
    :param t0_datas: startimes of the other waveforms in s
    :param norm: normalize correlation to the range [-1 1] in the time domain
    :param centered: center the output ccf array on 0, see ccflagtime
    :return ccf_lagtime, fftccf_arrays:

    lagtime convention : similar to the fft frequency axis wrapping
        centered:
            if nfft is even (dt=1) (0 goes with positive lags)
                 lagtime        -3  -2  -1   0   1   2
                 ifft(ccf)       |   |   |   |   |   |
            if nfft is odd (dt=1) (symetrical relative to the 0)
                 lagtime        -2  -1   0   1   2
                 ifft(ccf)       |   |   |   |   |

            => get the positive lags with the 0 using ifft(ccf)[nfft//2:]
            => get the negative lags without the 0 using ifft(ccf)[:nfft//2]
            => to truncate the lagtime axis one can remove the same number of samples each side of the ccf
                ccf1 = ifft(ccf)[n:-n]
                whatever if nfft is odd or even

        not centered:
            if nfft is even (dt=1) (0 goes with positive lags)
                 lagtime         0   1   2  -3  -2  -1
                 ifft(ccf)       |   |   |   |   |   |
            if nfft is odd (dt=1)
                 lagtime         0   1   2  -2  -1
                 ifft(ccf)       |   |   |   |   |

            => get the positive lags with the 0 using ifft(ccf)[:(nfft//2 + nfft%2)]
            => get the negative lags without the 0 using ifft(ccf)[(nfft//2 + nfft%2):]
            => to truncate the lagtime axis one can keep the same number of samples each side of the ccf
                ccf1 = hstack((ifft(ccf)[:n], ifft(ccf)[-n:]))
                whatever if nfft is odd or even
    """
    if not fft_datas.ndim == 2:
        raise ValueError(f"fft_datas must be 2d array, got shape {fft_datas.shape}")
    nsta, nfft = fft_datas.shape

    if fft_datas_ref.ndim == 1:
        if not fft_datas_ref.shape == (nfft,):
            raise ValueError(f"if fft_data_ref is a 1d array, "
                             f"it must have the same number of frequency samples as fft_datas ({fft_datas.shape[1]})"
                             f", got {fft_datas_ref.shape}")
        nref = 1
    elif fft_datas_ref.ndim == 2:
        if not fft_datas_ref.shape == fft_datas.shape:
            raise ValueError(f"if fft_data_ref is a 2d array, "
                             f"it must have the same shape as fft_datas ({fft_datas.shape})"
                             f", got {fft_datas_ref.shape}")
        nref = nsta
    else:
        raise ValueError(f'bad number of dimensions for fft_datas_ref ({fft_datas_ref.shape})')

    if isinstance(t0_datas, float):
        t0_datas = np.ones(nsta, float) * t0_datas

    if isinstance(t0_datas_ref, float):
        t0_datas_ref = np.ones(nref, float) * t0_datas_ref

    t0_datas: np.ndarray  # shape (nsta, )
    t0_datas_ref: np.ndarray  # shape (nref, )

    freqs = fftfreq(nfft, delta)

    # ========== correlation
    # simple correlation, no padding, mind the temporal overlapping
    # if the time support is too large...
    fft_datas_ref_conj = fft_datas_ref.conj()
    fftccf_arrays = fft_datas * fft_datas_ref_conj  # NOT NORMALIZED!
    assert fftccf_arrays.shape == fft_datas.shape, "unexpected shape"

    if norm:
        """
        let U and V be two complex signals out of fft, length N, vertical vectors
        notations : 
            . = scalar product
            ^* = conjugate
            ^t = transpose
            | x | = modulus of x
            || X || = norm of vector X = sqrt( X^t* . X )

        the Cauchy-Schwartz relation states that       
            |U^t* . V| <= || U || * || V || = sqrt( (U^t* . U) * (V^t* . V) )  (a real scalar)

            thus 

            |  [U^t* / sqrt(U^t* . U)] . [V /  sqrt(V^t* . V)]  | <= 1

        let    C = N * [U^t* / sqrt(U^t* . U)] * [V /  sqrt( V^t* . V)]  (term by term product)
        then   | sum_over_i (Ci) | / N <= 1

        knowing that ifft(C)[i=0] = 1/N sum_over_k ( Ck * exp(0) )
        then | ifft(C)[i=0] | <= 1

        the ifft of the correlation function C at lag time 0 is bounded to the range [-1, 1]
        TODO: demonstrate that this holds true for any lagtime            
        """
        if nref == 1:
            a = (fft_datas_ref * fft_datas_ref_conj).real.sum() ** 0.5
        elif nref == nsta:
            a = (fft_datas_ref * fft_datas_ref_conj).real.sum(axis=1)[:, np.newaxis] ** 0.5
        else:
            raise ValueError('should not happen')
        del fft_datas_ref_conj
        b = (fft_datas * fft_datas.conj()).real.sum(axis=1)[:, np.newaxis] ** 0.5

        normalization_factor = a * b / float(nfft)
        normalization_factor[normalization_factor == 0.] = 1.0  # if a or b is 0 => correlation will be 0 anyway
        fftccf_arrays /= normalization_factor

    if derivate:
        fftccf_arrays *= 2.j * np.pi * freqs

    # apply the time correction due to the different statrttimes
    starttime_corrections: np.ndarray = t0_datas - t0_datas_ref

    if centered:
        # wrap the ccf so that the correlation is centered on 0
        lagtime_start = -(nfft // 2) * delta
    else:
        # return the raw correlation, first sample corresponds to lag 0
        # ccf_lagtime will be irregular to get accurate lag times even on negative side
        lagtime_start = 0.

    time_shifts = starttime_corrections - lagtime_start
    if time_shifts.any():
        spectral_shifts = exp(-2.j * np.pi * freqs * time_shifts[:, np.newaxis])
        fftccf_arrays *= spectral_shifts

    if centered:
        ccf_lagtime = np.arange(nfft) * delta + lagtime_start
    else:
        ccf_lagtime = fftfreq(nfft, 1. / nfft) * delta

    return ccf_lagtime, fftccf_arrays


def fft_correlate(
        fft_data_ref: np.ndarray, fft_data: np.ndarray,
        delta: float,
        t0_data_ref: float = 0., t0_data: float = 0.,
        norm: bool = False,
        centered: bool = True,
        derivate: bool = False) \
        -> (np.ndarray, np.ndarray):
    """
    :param fft_data_ref: 1d array, the fft of the reference waveform
    :param fft_data: 1d array, the fft of all the waveforms to correlate with the reference
    :param delta: sampling interval in s, same for all waveforms
    :param t0_data_ref: starttime of the reference wavefrom in s
    :param t0_data: startime of the other waveform in s
    :param norm: normalize correlation to the range [-1 1] in the time domain
    :param centered: center the output ccf array on 0, see ccflagtime
    :return ccf_lagtime, fftccf_array:
    """

    ccf_lagtime, fftccf_arrays = fft_correlate_many(
        fft_datas_ref=fft_data_ref,
        fft_datas=fft_data[np.newaxis, :],
        delta=delta,
        t0_datas_ref=t0_data_ref,
        t0_datas=np.array([t0_data]),
        norm=norm, centered=centered,
        derivate=derivate)

    return ccf_lagtime, fftccf_arrays[0, :]


def correlate_many(
        datas_ref: Union[list, np.ndarray],
        datas: list,
        delta: float,
        npad: int,
        t0_datas_ref: Union[float, np.ndarray] = 0.,
        t0_datas: Union[float, np.ndarray] = 0.,
        use_next_fast_len: bool = True,
        norm: bool = False,
        centered: bool = True,
        derivate: bool = False):
    """

    """

    if isinstance(datas_ref, list):
        if not np.all([isinstance(data_ref, np.ndarray) for data_ref in datas_ref]):
            raise TypeError(f"datas_ref is not a list of 1d np.ndarrays")

        if not np.all([data_ref.ndim == 1 for data_ref in datas_ref]):
            raise TypeError(f"datas_ref is not a list of 1d np.ndarrays")

    elif isinstance(datas_ref, np.ndarray):
        assert datas_ref.dtype in [float, complex], datas_ref.dtype

        if datas_ref.ndim == 1:
            datas_ref = [datas_ref]

        elif datas_ref.ndim == 2:
            assert len(datas_ref) == len(datas)
            datas_ref = [data for data in datas_ref]

        else:
            raise ValueError

    else:
        raise TypeError('unexpected input types')
    datas_ref: list

    # nsta = len(datas)
    # nref = len(datas_ref)

    nptsmax = max([len(data) for data in datas] + [len(data) for data in datas_ref])
    nfft = nptsmax + npad

    if use_next_fast_len:
        nfft = next_fast_len(nfft)

    fft_datas_ref = np.asarray([fft(data, nfft) for data in datas_ref], complex)
    fft_datas = np.asarray([fft(data, nfft) for data in datas], complex)

    if len(fft_datas_ref) == 1:
        print(fft_datas_ref.shape)
        fft_datas_ref = fft_datas_ref[0]
        assert isinstance(fft_datas_ref, np.ndarray)
        assert fft_datas_ref.ndim == 1

    ccf_lagtime, fftccf_arrays = fft_correlate_many(
        fft_datas_ref=fft_datas_ref,
        fft_datas=fft_datas,
        delta=delta,
        t0_datas_ref=t0_datas_ref,
        t0_datas=t0_datas,
        norm=norm,
        centered=centered,
        derivate=derivate)

    # safety trim
    i_ccf_trim = ccf_trim(nlag=npad, nfft=nfft, centered=centered)
    ccf_lagtime = ccf_lagtime[i_ccf_trim]
    ccf_arrays = ifft(fftccf_arrays, axis=1).real[:, i_ccf_trim]

    return ccf_lagtime, ccf_arrays


def correlate(
        data_ref: np.ndarray,
        data: np.ndarray,
        delta: float,
        npad: int,
        t0_data_ref: float = 0.,
        t0_data: float = 0.,
        use_next_fast_len: bool = True,
        norm: bool = False,
        centered: bool = True,
        derivate: bool = False):
    ccf_lagtime, ccf_arrays = correlate_many(
        datas_ref=data_ref,
        datas=[data],
        delta=delta,
        npad=npad,
        t0_datas_ref=t0_data_ref,
        t0_datas=t0_data,
        use_next_fast_len=use_next_fast_len,
        norm=norm,
        centered=centered,
        derivate=derivate)

    return ccf_lagtime, ccf_arrays[0, :]


def visual_correlate(top=10, gain=0.1, **kwargs):
    delta = kwargs['delta']
    data_ref = kwargs['data_ref']
    data = kwargs['data']
    t_data_ref = kwargs['t0_data_ref'] + np.arange(len(data_ref)) * delta
    t_data = kwargs['t0_data'] + np.arange(len(data)) * delta

    ccf_lagtime, ccf_array = correlate(**kwargs)
    ccf_lagtime_argtmax, ccf_array_max_values = hypermax_multi(ccf_lagtime, ccf_array)
    ccf_lagtime_argtmin, ccf_array_min_values = hypermin_multi(ccf_lagtime, ccf_array)

    ccf_lagtime_argt = np.hstack((ccf_lagtime_argtmax, ccf_lagtime_argtmin))
    ccf_array_values = np.hstack((ccf_array_max_values, ccf_array_min_values))

    # select top correlation or anticorrelation points
    i = np.argsort(np.abs(ccf_array_values))[::-1][:top]
    ccf_array_values = ccf_array_values[i]
    ccf_lagtime_argt = ccf_lagtime_argt[i]

    # order by lagtime
    i = np.argsort(ccf_lagtime_argt)
    ccf_array_values = ccf_array_values[i]
    ccf_lagtime_argt = ccf_lagtime_argt[i]

    fig = plt.figure()
    gs = fig.add_gridspec(3, 1)
    ax0 = fig.add_subplot(gs[0, :])
    ax1 = fig.add_subplot(gs[1:, :], sharex=ax0)
    ax1.invert_yaxis()

    ax0.plot(ccf_lagtime, ccf_array, "k")

    gain /= np.max([data.std(), data_ref.std()])
    # gain = (ccf_lagtime.max() - ccf_lagtime.min()) / np.median(ccf_lagtime_argt[1:] - ccf_lagtime_argt[:-1])
    gain *= np.median(ccf_lagtime_argt[1:] - ccf_lagtime_argt[:-1])  # (ccf_lagtime.max() - ccf_lagtime.min())

    # offset = 0.0
    # ax1.plot(gain * data_ref + offset, t_data_ref, 'r')
    # ax1.plot(gain * data + offset, t_data, 'k')

    for offset, c in zip(ccf_lagtime_argt, ccf_array_values):
        print(offset, gain * np.sign(c))
        ax1.plot(gain * data_ref + offset, t_data_ref, 'r')
        if c >= 0:
            ax0.plot(offset, c, 'ks')
            ax1.plot(gain * np.sign(c) * data + offset, t_data - offset, 'k')
        else:
            ax0.plot(offset, c, 'bs')
            ax1.plot(gain * np.sign(c) * data + offset, t_data - offset, 'b')

    ax0.grid(True)
    ax1.grid(True)

    return fig


# def fft_correlate_all_with_all_old(
#         fft_datas: np.ndarray,
#         delta: float,
#         t0_datas: Union[float, np.ndarray]=0.,
#         norm: bool = False,
#         centered: bool = True,
#         derivate: bool = False):
#
#     """the old version of the function
#     using a double loop, slower because some operations
#     are repeated at each loop unnecessarily
#     """
#     nsta, nfft = fft_datas.shape
#
#     if isinstance(t0_datas, float):
#         t0_datas = np.ones(nsta) * t0_datas
#
#     for i in range(nsta - 1):
#         ccf_lagtime, fftccf_arrays = fft_correlate_many(
#             fft_datas_ref=fft_datas[i, :],
#             fft_datas=fft_datas[i + 1:, :],
#             delta=delta,
#             t0_datas_ref=t0_datas[i],
#             t0_datas=t0_datas[i + 1:],
#             norm=norm,
#             centered=centered,
#             derivate=derivate)
#
#         if i == 0:
#             yield ccf_lagtime  # first item yielded
#
#         for n, j in enumerate(range(i + 1, nsta)):
#             yield i, j, fftccf_arrays[n, :]


def fft_correlate_all_with_all(
        fft_datas: np.ndarray,
        delta: float,
        t0_datas: Union[float, np.ndarray] = 0.,
        norm: bool = False,
        centered: bool = True,
        derivate: bool = False):
    """
    correlate all trace in fft_datas with all others
    except autocorrelations
    I explore the upper triangle part of the cross spectral matrix


          0   1   2   3   4     <= index of the row in fft_datas to
                                   use for the second trace correlated
        ---------------------
     0  |   | 0 | 1 | 2 | 3 |   <= numbers in the cells indicate
        ---------------------      the order in which I generate
     1  |   |   | 4 | 5 | 6 |      cross correlations
        ---------------------      (NB the first item yielded is the
     2  |   |   |   | 7 | 8 |       lagtime array)
        ---------------------
     3  |   |   |   |   | 9 |
        ---------------------
     4  |   |   |   |   |   |
        ---------------------
     ^ Index of the row in fft_datas to use as the first trace correlated

    :param fft_datas: one row per fft trace
    :param delta: sampling interval in s
    :param t0_datas: starttime in s
    :param norm: if correlation is normalized
    :param centered: if lagtime is centered
    :param derivate: if ccf must be derivated in fourier domain
    :return: generator
        first item yielded is the ccf lagtime
    """

    nsta, nfft = fft_datas.shape

    if isinstance(t0_datas, float):
        t0_datas = np.ones(nsta) * t0_datas

    first_trace_indexs = np.concatenate([k * np.ones(nsta - 1 - k, int) for k in range(nsta - 1)])
    second_trace_indexs = np.concatenate([np.arange(k + 1, nsta) for k in range(nsta - 1)])

    # make sure the indexs above correspond to the double loop syntax
    # remove when sure it is ok
    n = 0
    for itest in range(nsta - 1):
        for jtest in range(itest + 1, nsta):
            assert itest == first_trace_indexs[n]
            assert jtest == second_trace_indexs[n]
            n += 1

    ccf_lagtime, fftccf_arrays = fft_correlate_many(
        fft_datas_ref=fft_datas[first_trace_indexs, :],
        fft_datas=fft_datas[second_trace_indexs, :],
        delta=delta,
        t0_datas_ref=t0_datas[first_trace_indexs],
        t0_datas=t0_datas[second_trace_indexs],
        norm=norm,
        centered=centered,
        derivate=derivate)

    yield ccf_lagtime  # first item yielded

    for n in range(fftccf_arrays.shape[0]):
        yield first_trace_indexs[n], second_trace_indexs[n], fftccf_arrays[n, :]


def solve_linear_system(dt_array: np.ndarray,
                        cc_array: np.ndarray,
                        tunc_min: float = 0.01,
                        tunc_max: float = 0.1,
                        tunc_alpha: float = 1,
                        iref: int = 0,
                        tpriorunc: float = 0.1) \
        -> (np.ndarray, np.ndarray):
    nsta = dt_array.shape[0]
    assert dt_array.shape == (nsta, nsta)
    assert cc_array.shape == (nsta, nsta)
    assert tunc_max >= tunc_min > 0
    assert tunc_alpha > 0

    nupper = (nsta - 1) * nsta // 2
    k = 0  # cell number in the upper part of tmaxs and amaxs
    Dtobs = np.zeros(nupper, float)
    Dtunc = np.zeros(nupper, float)

    Grows = []
    Gcols = []
    Gvals = []
    for i in range(nsta - 1):
        for j in range(i + 1, nsta):
            Grows.append(k)
            Grows.append(k)
            Gcols.append(i)
            Gcols.append(j)
            Gvals.append(-1.0)
            Gvals.append(+1.0)

            Dtobs[k] = dt_array[i, j]
            Dtunc[k] = (tunc_max - tunc_min) * (1. - cc_array[i, j]) ** tunc_alpha + tunc_min
            k += 1
    G = sp.csc_matrix((Gvals, (Grows, Gcols)), shape=(nupper, nsta))

    # Tprior = dt_array[iref, :]  # np.zeros(nsta, float)
    Tprior = np.zeros(nsta, float)
    CDtinv = sp.diags(Dtunc ** -2.0, format="csc")
    CMtinv = tpriorunc ** -2. * sp.diags(np.ones(nsta, float), format="csc")
    T = Tprior + splinalg.spsolve((G.T * CDtinv * G + CMtinv), (G.T * (CDtinv * (Dtobs - G * Tprior))))
    T = T - T[iref]

    # GT = np.zeros_like(dt_array)
    # ttt = G * T
    # k = 0
    # for i in range(nsta-1):
    #     for j in range(i+1, nsta):
    #         GT[i, j] = ttt[k]
    #         GT[j, i] = -ttt[k]
    #         k += 1
    # plt.figure()
    # plt.subplot(131)
    # plt.imshow(dt_array, vmin=-np.abs(dt_array).max(), vmax=np.abs(dt_array).max(), cmap=plt.get_cmap('RdBu'))
    # plt.subplot(132, sharex=plt.gca(), sharey=plt.gca())
    # plt.imshow(GT, vmin=-np.abs(dt_array).max(), vmax=np.abs(dt_array).max(), cmap=plt.get_cmap('RdBu'))
    # plt.subplot(133, sharex=plt.gca(), sharey=plt.gca())
    # plt.imshow(dt_array - GT, vmin=-np.abs(dt_array).max(), vmax=np.abs(dt_array).max(), cmap=plt.get_cmap('RdBu'))
    # plt.figure()
    # for _ in range(dt_array.shape[0]):
    #     plt.plot(dt_array[_, ...], 'k', alpha=0.1)
    # plt.plot(T, 'r')
    # plt.show()

    return T


def dt_cc_arrays(
        datas: list,
        delta: float,
        npad: int,
        use_next_fast_len: bool = True,
        t0_datas: Union[float, np.ndarray] = 0,
        dt_prior: float = 0.,
        show=False):
    """DEAD END ! """
    nsta = len(datas)
    nmax = max([len(data) for data in datas])
    nfft = nmax + npad
    if use_next_fast_len:
        nfft = next_fast_len(nfft)

    fft_datas = np.asarray([fft(data, nfft) for data in datas], complex)

    dt_array = np.zeros((nsta, nsta), float)
    cc_array = np.eye(nsta, dtype=float)

    centered = True
    generator = fft_correlate_all_with_all(
        fft_datas=fft_datas,
        delta=delta,
        t0_datas=t0_datas,
        norm=True,
        centered=centered)

    ccf_lagtime: np.ndarray = next(generator)

    i_ccf_trim = ccf_trim(nlag=npad, nfft=nfft, centered=centered)
    ccf_lagtime_trim = ccf_lagtime[i_ccf_trim]

    if dt_prior > 0:
        prior_taper_trim = np.exp(-0.5 * (ccf_lagtime_trim / dt_prior) ** 2.0)
    else:
        prior_taper_trim = 1.0

    for i, j, fft_ccf_array in generator:
        ccf_array_trim = ifft(fft_ccf_array).real[i_ccf_trim] * prior_taper_trim

        dtij = hypermax(t=ccf_lagtime_trim, f=ccf_array_trim)
        cc = np.interp(dtij, xp=ccf_lagtime_trim, fp=ccf_array_trim)
        dt_array[i, j] = +dtij
        dt_array[j, i] = -dtij
        cc_array[i, j] = cc_array[j, i] = cc

    if show:
        plt.figure()
        ax1 = plt.subplot(121)
        ax2 = plt.subplot(122, sharex=ax1, sharey=ax1)

        plt.colorbar(
            ax1.imshow(
                dt_array,
                vmin=-np.abs(dt_array).max(),
                vmax=+np.abs(dt_array).max(),
                cmap=plt.get_cmap('jet')), ax=ax1)

        plt.colorbar(
            ax2.imshow(
                cc_array,
                vmin=-1.0,
                vmax=+1.0,
                cmap=plt.get_cmap('RdBu')), ax=ax2)
        # plt.show()

    return dt_array, cc_array


def similarty(cc_array):
    """objective = order the items that are similar to each other using the cc_array"""
    pass


if __name__ == '__main__':

    # A = fft(np.random.randn(250, 301), axis=1)
    # g1 = fft_correlate_all_with_all_old(
    #     fft_datas=A,
    #     t0_datas=np.arange(250)*0.1,
    #     delta=0.123456,
    #     )
    # g2 = fft_correlate_all_with_all(
    #     fft_datas=A,
    #     t0_datas=np.arange(250) * 0.1,
    #     delta=0.123456,
    #     )
    #
    # from proton.timer import Timer
    # with Timer() as tm:
    #     g1 = list(g1)
    #     tm.checkpoint('1')
    #     g2 = list(g2)
    # assert len(g1) == len(g2)
    #
    # t1 = g1.pop(0)
    # t2 = g2.pop(0)
    # assert t1.shape == t2.shape
    # assert (t1 == t2).all()
    # for (i1, j1, f1), (i2, j2, f2) in zip(g1, g2):
    #     assert i1 == i2
    #     assert j1 == j2
    #     assert f1.shape == f2.shape
    #     assert (f1 == f2).all()
    #
    # exit(0)

    from sigy.signal.xcorrfft import xcorrfft_exact

    dt = 0.0123
    tshift = 7.21 * dt

    data1 = np.random.randn(256)
    data2 = data1.copy()

    nu = fftfreq(len(data1), dt)
    data2 = 2. * ifft(fft(data2) * np.exp(-2.j * np.pi * nu * tshift)).real * -1.

    # data2 += 1.1 * np.random.randn(len(data2))
    # data2 = data2[:1000]

    fig = visual_correlate(
        data_ref=data1,
        data=data2,
        delta=dt,
        t0_data_ref=0.0,
        t0_data=0.0,
        npad=512)

    plt.show()

    plt.figure()
    plt.subplot(211)
    plt.plot(data1)
    plt.plot(data2)

    dataout, lagtime = xcorrfft_exact(data1=data2, data2=data1, dt=dt, normalize=True)

    plt.subplot(212)
    plt.plot(lagtime, dataout, linewidth=3)

    for pad in [100]:
        fft_data1 = fft(data1, len(data1) + pad)
        fft_data2 = fft(data2, len(data2) + pad)

        ccf_lagtime, fft_ccf12 = fft_correlate(
            fft_data_ref=fft_data1,
            fft_data=fft_data2,
            delta=dt,
            norm=True,
            centered=True)

        print(ccf_lagtime)
        i = ccf_trim(nlag=100, nfft=len(data1) + pad, centered=True)

        print(i)
        ccf12 = ifft(fft_ccf12).real
        plt.plot(ccf_lagtime, ccf12, 'k')
        plt.plot(ccf_lagtime[i], ccf12[i], 'g')

    plt.plot(tshift * np.ones(2), plt.gca().get_ylim(), 'r--')

    plt.show()
