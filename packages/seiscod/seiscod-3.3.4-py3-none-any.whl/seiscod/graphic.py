from typing import Union
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
from seiscod.trace import Trace, FFTTrace
from tempoo.timetick import timetick
from seiscod.signal.hypermax import isolate_sections_with_same_sign


"""
segments designate a list of 2D arrays 
each array having xdata in first column and ydata in second column
"""


def _get_segments_xbounds(segments):
    if not len(segments) or sum([seg.size for seg in segments]) == 0:
        return 0., 1.

    xmin, xmax = np.inf, -np.inf
    for seg in segments:
        if seg.size:
            xmin = min([xmin, seg[:, 0].min()])
            xmax = max([xmax, seg[:, 0].max()])

    return xmin, xmax


def _get_segments_ybound(segments):
    if not len(segments) or sum([seg.size for seg in segments]) == 0:
        return 0., 1.

    ymin, ymax = np.inf, -np.inf
    for seg in segments:
        if seg.size:
            ymin = min([ymin, seg[:, 1].min()])
            ymax = max([ymax, seg[:, 1].max()])
    return ymin, ymax


def _swap_segments_xy(segments):
    j = np.array([1, 0], int)
    return [seg[:, j] for seg in segments]


def _get_stream_segments_fourier_domain(stream, gain, gain_mode, offsets, doffset_med, clip_display):

    stream_segments = []

    # get moduli, positive freqs
    fs, dats = [], []
    for i, tr in enumerate(stream):
        f, dat = tr.side(sign=1, zero=False, copy=False)
        fs.append(f)
        dats.append(np.abs(dat))

    if gain_mode == "relative":
        amplitude_scaling_coeff = gain / np.std(np.hstack(dats)) * doffset_med
    elif gain_mode == "absolute":
        amplitude_scaling_coeff = gain
    else:
        raise ValueError(gain_mode)

    for i, (f, ydat) in enumerate(zip(fs, dats)):
        xdat = f
        ydat = amplitude_scaling_coeff * ydat + offsets[i]

        if clip_display:
            ydat = np.clip(ydat - offsets[i], -doffset_med, doffset_med) + offsets[i]

        dat = np.column_stack((xdat, ydat))
        stream_segments.append(dat)

    return stream_segments


def _get_stream_segments_time_domain(stream, gain, gain_mode, offsets, doffset_med, clip_display, obspy_decim, obspy_decim_nwin):

    if gain_mode == "relative":
        std = stream.std()
        amplitude_scaling_coeff = gain / (std if std != 0. else 1.) * doffset_med
        # print('???', gain, std, doffset_med, amplitude_scaling_coeff)

    elif gain_mode == "absolute":
        amplitude_scaling_coeff = gain

    else:
        raise ValueError(gain_mode)

    stream_segments = []

    for i, tr in enumerate(stream):
        if obspy_decim:
            t, ydat = tr.obspy_like_decim(nwin=obspy_decim_nwin)
            xdat = t
            ydat = amplitude_scaling_coeff * ydat + offsets[i]

        else:
            xdat = tr.atime()
            ydat = amplitude_scaling_coeff * tr.data + offsets[i]

        if clip_display:
            ydat = np.clip(ydat - offsets[i], -doffset_med/2, doffset_med/2) + offsets[i]

        dat = np.column_stack((xdat, ydat))
        stream_segments.append(dat)

    return stream_segments


def _get_stream_face_and_color_segments_time_domain(stream, gain, gain_mode, offsets, doffset_med, clip_display, facecolor):

    if gain_mode == "relative":
        std = stream.std()
        amplitude_scaling_coeff = gain / (std if std != 0. else 1.) * doffset_med

    elif gain_mode == "absolute":
        amplitude_scaling_coeff = gain

    else:
        raise ValueError(gain_mode)

    stream_face_segments = []
    stream_face_colors = []
    if len(facecolor) == 1:
        twocolors = False
        colorsups = [facecolor for _ in range(len(stream))]
        colorinfs = [None for _ in range(len(stream))]

    elif len(facecolor) == 2:
        twocolors = True
        colorsups = [facecolor[0] for _ in range(len(stream))]
        colorinfs = [facecolor[1] for _ in range(len(stream))]

    elif len(facecolor) == len(stream):
        twocolors = False
        colorsups = facecolor
        colorinfs = [None for _ in range(len(stream))]

    else:
        raise ValueError(facecolor, "not understood")

    for i, trace in enumerate(stream):
        gen = isolate_sections_with_same_sign(
            t=trace.atime(), f=trace.data,
            assume_t_growing=True)

        for sign, tim, dat in gen:
            if sign < 0 and not twocolors:
                # do not color negative segments
                continue

            xdat = tim
            ydat = amplitude_scaling_coeff * dat + offsets[i]

            if clip_display:
                ydat = np.clip(ydat - offsets[i], -doffset_med/2, doffset_med/2) + offsets[i]

            dat = np.column_stack((xdat, ydat))
            stream_face_segments.append(dat)
            if twocolors:
                if sign > 0:
                    stream_face_colors.append(colorsups[i])
                else:
                    stream_face_colors.append(colorinfs[i])
            else:
                stream_face_colors.append(colorsups[i])

    return stream_face_segments, stream_face_colors


def _get_stream_positive_segments_fourier_domain(stream, gain, gain_mode, offsets, doffset_med, clip_display):
    stream_std = np.hstack([np.abs(trace.data) for trace in stream]).std()

    if gain_mode == "relative":
        amplitude_scaling_coeff = gain / stream_std * doffset_med
    elif gain_mode == "absolute":
        amplitude_scaling_coeff = gain
    else:
        raise ValueError(gain_mode)

    stream_positive_segments = []

    for i, trace in enumerate(stream):
        trace: FFTTrace
        xdat, dat = trace.side(sign=1, copy=False)
        ydat = amplitude_scaling_coeff * np.abs(dat) + offsets[i]

        # repeate first and last points to make sure the filled area starts at level offsets[i]
        xdat = np.hstack((xdat[0], xdat, xdat[-1]))
        ydat = np.hstack((offsets[i], ydat, offsets[i]))

        if clip_display:
            ydat = np.clip(ydat - offsets[i], -doffset_med, doffset_med) + offsets[i]

        dat = np.column_stack((xdat, ydat))
        stream_positive_segments.append(dat)

    return stream_positive_segments


def _get_segments(stream, alpha, facealpha, facecolor, fourier_domain, gain, gain_mode, clip_display, offsets, doffset_med, obspy_decim,
                  obspy_decim_nwin):
    stream_edge_segments = []
    stream_face_segments = []
    stream_face_colors = []

    if fourier_domain:
        if alpha:
            stream_edge_segments = \
                _get_stream_segments_fourier_domain(
                    stream, gain, gain_mode, offsets, doffset_med, clip_display)

        if facealpha:
            stream_face_segments = \
                _get_stream_positive_segments_fourier_domain(
                    stream,
                    gain, gain_mode, offsets,
                    doffset_med, clip_display)
            if len(facecolor) == len(stream):
                stream_face_colors = facecolor
            elif len(facecolor) in [1, 2]:
                stream_face_colors = [facecolor[0] for _ in range(len(stream_face_segments))]
            else:
                raise ValueError(facecolor)

    else:
        if alpha:
            stream_edge_segments = \
                _get_stream_segments_time_domain(
                    stream,
                    gain, gain_mode, offsets,
                    doffset_med, clip_display,
                    obspy_decim, obspy_decim_nwin)

        if facealpha:
            stream_face_segments, stream_face_colors = \
                _get_stream_face_and_color_segments_time_domain(
                    stream,
                    gain, gain_mode, offsets,
                    doffset_med,
                    clip_display,
                    facecolor)
    return stream_edge_segments, stream_face_segments, stream_face_colors


def _get_trace_offsets(stream, ydim, seedticks, master_offset: float=0.):
    offset_ticks, offset_ticklabels = None, None

    if ydim == "trace":
        offsets = np.arange(len(stream))

    else:
        try:
            offsets = stream.get(ydim)
        except KeyError as e:
            raise ValueError('ydim must be trace or a key that exists in all traces of the stream ' + str(e))

        try:
            float(offsets[0])
        except ValueError:
            # offsets cannot be converted to float :
            # so I use the index of the offsets in the unique version of offsets
            _, offsets = np.unique(offsets, return_inverse=True)

    offsets = np.asarray(offsets, float) + float(master_offset)

    u_offsets = np.sort(np.unique(offsets))
    if len(u_offsets) > 1: # f"offsets must have different values, found only {u_offsets[0]}"
        doffset_med = np.median(u_offsets[1:] - u_offsets[:-1])
        assert doffset_med > 0, "offsets must have different values"
    else:
        doffset_med = max([tr.data.max() - tr.data.min() for tr in stream])  / 2.

    offsetmin = offsets.min() - doffset_med
    offsetmax = offsets.max() + doffset_med

    if seedticks:
        offset_ticks = offsets
        offset_ticklabels = stream.get('seedid')

    return offsets, doffset_med, offsetmin, offsetmax, offset_ticks, offset_ticklabels


def show_stream(stream, ax,
                gain: float=0.1,
                gain_mode: str="relative",
                color: Union[str, list]="k",
                alpha: float=0.4,
                linewidth: int=2, linestyle: str="-",
                facecolor: str="rb",  # two color letters = up/down, one letter = up only
                facealpha: float=0.,  # increase to activate the trace coloration
                obspy_decim: bool=False, obspy_decim_nwin: int=1000,
                clip_display: bool=False,
                ydim: str="trace",
                master_offset: float=0.,
                timeticks: bool=True,
                seedticks: bool=False,
                swapxy: bool = False,
                set_lim: bool = True,
                label: Union[None, str] = None,
                ):
    """
    :param stream: seiscod.stream.Stream object to display
    :param ax: matplotlib axe on which to display stream
    :param gain: amplification coefficient
        if gain_mode is "relative" (the default)
            the traces will be multiplied by gain * the median inter-trace / stream.std()
                to plot several streams (st1, st2) with the same gain use
                st1.show(ax, gain=0.1)
                st2.show(ax, gain=0.1 * st2.std() / st1.std())
        if gain_mode is "absolute":
            the traces will be multiplied by gain, user will have to adjuste the value
            it is more convenient to ensure comparable amplitudes when several streams are plotted
    :param color: line color
    :param alpha: line alpha
    :param linewidth:
    :param linestyle:
    :param facecolor: one or two color letters
    :param obspy_decim: decimate the piece of data displayed to increase performance
                        this feature mimics the obspy behavior for trace representation
    :param ydim: the dimension to use for inter-trace distances (by index, or by a given attribute)
                 use trace to display by trace index
                 otherwise please specify an attribute to use for offset
                 e.g. distance if all the traces in stream have a "distance" attribute
    :param master_offset: add a constant value to the traces offsets
    """

    # assert len(stream) > 1, len(stream)
    assert 0 <= alpha <= 1.0, f"alpha must be between 0 and 1; got {alpha}"
    assert 0 <= facealpha <= 1.0, f"alpha must be between 0 and 1; got {facealpha}"
    assert alpha or facealpha

    trace_offsets, doffset_med, offsetmin, offsetmax, offset_ticks, offset_ticklabels = \
        _get_trace_offsets(stream, ydim, seedticks, master_offset)

    fourier_domain = np.all([isinstance(tr, FFTTrace) for tr in stream])

    stream_edge_segments, stream_face_segments, stream_face_colors = \
        _get_segments(
            stream, alpha, facealpha, facecolor,
            fourier_domain, gain, gain_mode,
            clip_display, trace_offsets, doffset_med, obspy_decim,
            obspy_decim_nwin)

    if alpha:
        tmin, tmax = _get_segments_xbounds(stream_edge_segments)
    elif facealpha:
        tmin, tmax = _get_segments_xbounds(stream_face_segments)
    else:
        raise Exception('must not happen')

    if swapxy:
        stream_face_segments = _swap_segments_xy(stream_face_segments)
        stream_edge_segments = _swap_segments_xy(stream_edge_segments)

    facecoll = PolyCollection(
        stream_face_segments,
        facecolors=stream_face_colors,
        alpha=facealpha)

    edgecoll = LineCollection(
        stream_edge_segments, colors=color, alpha=alpha,
        linewidths=linewidth, linestyles=linestyle,
        label=label)

    ax.add_collection(facecoll)
    ax.add_collection(edgecoll)

    if seedticks:
        if swapxy:
            ax.set_xticks(offset_ticks)
            ax.set_xticklabels(offset_ticklabels)
        else:
            ax.set_yticks(offset_ticks)
            ax.set_yticklabels(offset_ticklabels)

    if timeticks and not fourier_domain:
        if tmax >= tmin : #  > 0:
            timetick(ax=ax, axis={True: "y", False: "x"}[swapxy],
                     major=True, minor=True)

    if set_lim:
        if swapxy:
            ax.set_ylim(tmin, tmax)
            ax.set_xlim(offsetmin, offsetmax)
        else:
            ax.set_xlim(tmin, tmax)
            ax.set_ylim(offsetmin, offsetmax)

    if swapxy:
        if not ax.yaxis_inverted():
            ax.invert_yaxis()

    plt.sca(ax)
    return trace_offsets


def shade_stream(stream, ax, cmap=None, vmin=None, vmax=None, powergain=1.,
                 seedticks=False, timeticks=True,
                 showcolorbar=True, swapxy=False,
                 ydim="trace",
                 set_lim: bool = True,
                 **kwargs):

    assert len(stream), len(stream)
    kwargs.setdefault('rasterized', True)

    fourier_domain = np.all([isinstance(tr, FFTTrace) for tr in stream])

    if cmap is None:
        if fourier_domain:
            cmap = plt.get_cmap('nipy_spectral')
        else:
            cmap = plt.get_cmap('gray')

    nmax = np.max([len(tr.data) for tr in stream])

    if ydim == "trace":
        offset_edges = np.arange(len(stream)+1) - 0.5
        offsets = np.arange(len(stream))

    else:
        offsets = stream.get(ydim)
        if (offsets[1:] < offsets[:-1]).any():
            raise ValueError('attribute used for ydim must be growing')

        elif (offsets[1:] == offsets[:-1]).any():
            # some offsets are repeated
            uoffsets, ioffsets, coffsets = \
                np.unique(
                    offsets, return_index=True,
                    return_inverse=False, return_counts=True)

            uoffset_edges = np.hstack((
                uoffsets[0] - 0.5 * (uoffsets[1] - uoffsets[0]),
                0.5 * (uoffsets[1:] + uoffsets[:-1]),
                uoffsets[-1] + 0.5 * (uoffsets[-1] - uoffsets[-2])))
            offset_edges = uoffset_edges

            min_bin_widths = \
                np.vstack((
                    uoffset_edges[1:] - uoffsets,
                    uoffsets - uoffset_edges[:-1])).min(axis=0)
            offsets = np.concatenate(
                [np.linspace(u - 0.1 * bw, u + 0.1 * bw, n)
                 for u, bw, n in zip(uoffsets, min_bin_widths, coffsets)])

        assert (offsets[1:] > offsets[:-1]).all()  # remove if ok, never crashed yet
        uoffsets = np.unique(offsets)   # sorted

        uoffset_edges = np.hstack((
            uoffsets[0] - 0.5 * (uoffsets[1] - uoffsets[0]),
            0.5 * (uoffsets[1:] + uoffsets[:-1]),
            uoffsets[-1] + 0.5 * (uoffsets[-1] - uoffsets[-2])))
        offset_edges = uoffset_edges

    T, I, D = [], [], []
    dmin, dmax = np.inf, -np.inf
    for n, tr in enumerate(stream):
        if fourier_domain:
            # use positive freqs and spectrum modulus
            f, d = tr.side(sign=1, zero=False, copy=False)
            d = np.abs(d)
        else:
            # take the time data array
            d = tr.data[:]

        if powergain != 1.:
            d = np.sign(d) * np.abs(d) ** powergain

        # all items in D must be the same length
        d = np.concatenate((d, np.nan * np.zeros(nmax - len(d))))
        d = np.ma.masked_where(np.isnan(d) | np.isinf(d), d)
        dmin = np.min([dmin, d.min()])
        dmax = np.max([dmax, d.max()])
        # -----
        D.append(d)
        if n <= len(stream) - 2:
            D.append(np.zeros_like(d))

        # -----
        if fourier_domain:
            # compute frequency edges
            df = f[1] - f[0]
            f = -.5 * df + np.hstack((f, (f[-1] + df) * np.ones(nmax + 1 - len(f))))
            T.append(f)
            T.append(f)
        else:
            # compute time edges
            dt = tr.delta
            t = -.5 * dt + tr.starttime + np.arange(nmax + 1) * dt
            T.append(t)
            T.append(t)
            del dt

        # -----
        I.append(offset_edges[n] * np.ones(len(d) + 1))
        I.append(offset_edges[n + 1] * np.ones(len(d) + 1))

    T, I, D = [np.asarray(_) for _ in [T, I, D]]
    if vmin is None and vmax is None:
        vmax = np.max([abs(dmin), abs(dmax)])
        vmin = -vmax
    if vmax is None:
        vmax = dmax
    if vmin is None:
        vmin = dmin

    if fourier_domain:
        vmin = 0.
        vmax = vmax

    if swapxy:
        X, Y, Z = I, T, D
    else:
        X, Y, Z = T, I, D

    coll = ax.pcolormesh(
        X, Y, Z,
        cmap=cmap,
        vmin=vmin, vmax=vmax,
        **kwargs)

    if seedticks:
        sticks = offsets  # np.arange(len(stream))
        sticklabels = [_.seedid for _ in stream]

        if swapxy:
            ax.set_xticks(sticks)
            ax.set_xticklabels(sticklabels)
        else:
            ax.set_yticks(sticks)
            ax.set_yticklabels(sticklabels)


    if set_lim:
        tmin, tmax = T.min(), T.max()
        offsetmin, offsetmax = I.min(), I.max()
        if swapxy:
            ax.set_ylim(tmin, tmax)
            ax.set_xlim(offsetmin, offsetmax)
        else:
            ax.set_xlim(tmin, tmax)
            ax.set_ylim(offsetmin, offsetmax)

    cax = None
    if showcolorbar:
        cbarwidth = 0.008
        cbarheight = 0.5
        cbardist = 0.012
        p = ax.get_position()
        cax = ax.figure.add_axes((p.x1 + cbardist * p.width,
                                  p.y0 + 0.5 * (1. - cbarheight) * p.height,
                                  cbarwidth, cbarheight * p.height))

        ax.figure.colorbar(coll, cax=cax, ticks=[vmin, 0, vmax])
        cax.set_yticklabels(["-", "0", "+"])

    if not fourier_domain and timeticks:
        if T.max() >= T.min() > 0:
            timetick(ax=ax, axis="y" if swapxy else "x", major=True, minor=True)

    if swapxy:
        if not ax.yaxis_inverted():
            ax.invert_yaxis()

    plt.sca(ax)
    return coll, cax


if __name__ == '__main__':
    from seiscod import *

    st = Stream()
    for _ in range(10):
        tr = Trace(data=np.random.randn(100), delta=1.0, starttime=np.random.randn())
        st.append(tr)
        if _ == 3:
            tr.data *= 0.
        if _ == 4:
            tr.data[2:] = 0.
        if _ == 5:
            tr.data[:-2] = 0.
    st.show(plt.gca(), facealpha=1.0, facecolor="gr")
    plt.show()
