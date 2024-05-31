from typing import Union
import matplotlib.pyplot as plt
import os.path

import numpy as np

DEFAULT_TIMEPICK: float = 12345.


class StreamPicker(object):

    def __init__(self, stream, ax,
                 trace_offsets: np.ndarray, verbose: bool=True,
                 swapxy: bool=False,
                 save_stream_as: Union[None, str] = None):
        """
        trace_offsets : the position of each trace in the plot
        """
        self.stream = stream
        self.ax = ax
        self.trace_offsets = trace_offsets
        self.swapxy = swapxy
        self.verbose = verbose

        self.pick_line_handles = []
        self.pick_text_handles = []

        self.connect()
        self.set_existing_picks()
        self.save_stream_as = save_stream_as
        if self.save_stream_as is not None:
            assert self.save_stream_as.endswith(".seiscodstream.npz")
            if os.path.isfile(self.save_stream_as):
                assert \
                    input(
                        f"WARNING : {self.save_stream_as} exists already, "
                        f"OVERWRITING IT WILL REMOVE "
                        f"ALL THE ADDITIONAL KEYS NOT LOADED, "
                        f"continue?") == "y"

        if self.verbose:
            # os.system(r"""notify-send -i terminal "p=pick u=unpick q=quit" """)
            help = "t=pick " \
                   "i=interpolate_picks " \
                   "w=propagate picks forward by correlation " \
                   "u=undo_last_pick " \
                   "r=remove_all_picks " \
                   "p=prompt " \
                   "j=save_picks_only " \

            if self.save_stream_as is not None:
                help += f"o=save_stream_as[{self.save_stream_as}] "

            help += "q=quit "
            print("\t" + "\n\t".join(help.split()))

    def connect(self):
        plt.ioff()
        self.ax.figure.canvas.draw()
        self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.figure.canvas.mpl_connect('key_press_event', self)

    def set_existing_picks(self):
        """load the picks from the header (timepick)"""
        for trace, trace_offset in zip(self.stream, self.trace_offsets):
            if hasattr(trace, 'timepick') and trace.timepick != DEFAULT_TIMEPICK:
                self.add_pick(trace.timepick, trace_offset)
            else:
                trace.timepick = DEFAULT_TIMEPICK
        self.refresh()

    def __call__(self, event):

        if event.inaxes is not self.ax:
            raise Exception('out')

        if event.key in ['t', 'd']:
            if self.swapxy:
                yvalue, timepick = event.xdata, event.ydata
            else:
                timepick, yvalue = event.xdata, event.ydata
            # find in the trace offsets which one is the closest from the pick
            trace_offset = self.trace_offsets[np.argmin(np.abs(self.trace_offsets - yvalue))]

            # find the traces that have been picked
            # nb: there might be more than one trace plotted at this position
            mask = np.isclose(self.trace_offsets, trace_offset)

            for traceindex, trace in enumerate(self.stream):
                if mask[traceindex]:
                    if event.key == "t":
                        self.del_pick(trace.timepick, trace_offset)

                        trace.__setattr__('timepick', timepick)
                        if self.verbose:
                            print(f"{trace}: pick at {timepick:.9f}")

                    elif event.key == "d" and trace.timepick != DEFAULT_TIMEPICK:
                        timepick = trace.timepick  # overwrite pick by existing one for del_picks
                        trace_offset = self.trace_offsets[traceindex]
                        trace.__setattr__('timepick', DEFAULT_TIMEPICK)
                        if self.verbose:
                            print(f"{trace}: delete pick at {timepick:.9f}")

                        self.del_pick(timepick, trace_offset)

            if event.key == "t":
                self.add_pick(timepick, trace_offset)

        if event.key == "i":
            _timepicks, _traceoffsets = self.get_picks()

            if len(_timepicks):
                isort = np.argsort(_traceoffsets)
                interp_timepicks = \
                    np.interp(self.trace_offsets,
                              xp=np.asarray(_traceoffsets)[isort],
                              fp=np.asarray(_timepicks)[isort],
                              left=DEFAULT_TIMEPICK,
                              right=DEFAULT_TIMEPICK)

                for n, (t, o) in enumerate(zip(interp_timepicks, self.trace_offsets)):
                    trace = self.stream[n]
                    if t != DEFAULT_TIMEPICK:
                        trace.__setattr__('timepick', t)
                        if self.verbose:
                            print(f"{trace}: pick at {t:.9f}")

                        self.add_pick(t, o)

        elif event.key == "w":
            if self.swapxy:
                yvalue, timepick = event.xdata, event.ydata
            else:
                timepick, yvalue = event.xdata, event.ydata

            # find in the trace offsets which one is the closest from the pick
            i_trace = np.argmin(np.abs(self.trace_offsets - yvalue))
            trace_offset = self.trace_offsets[i_trace]

            # find the traces that have been picked
            # nb: there might be more than one trace plotted at this position
            if np.isclose(self.trace_offsets, trace_offset).sum() > 1:
                print('there where more than one trace at this position')

            else:
                trace_picked = self.stream[i_trace]

                self.del_pick(trace_picked.timepick, trace_offset)
                trace_picked.__setattr__('timepick', timepick)
                if self.verbose:
                    print(f"{trace_picked}: pick at {timepick:.9f}")
                self.add_pick(timepick, trace_offset)

                if i_trace < len(self.stream)-1:
                    from seiscod.signal.correlate import correlate, hypermax
                    give_up = 0
                    for j_trace in range(i_trace+1, i_trace+30):
                        trace_j = self.stream[j_trace]
                        trace_offset_j = self.trace_offsets[j_trace]

                        # if hasattr(trace_j, "timepick") and  trace_j.timepick != DEFAULT_TIMEPICK:
                        #     print('--')
                        #     continue

                        if trace_j.delta == trace_picked.delta:
                            ccf_lagtime, ccf_data = correlate(
                                    data_ref=trace_picked.data.astype(float),
                                    data=trace_j.data.astype(float),
                                    delta=trace_picked.delta,
                                    npad=trace_picked.npts // 4,
                                    t0_data_ref=trace_picked.starttime,
                                    t0_data=trace_j.starttime,
                                    norm=True)
                            if ccf_data.max() < 0.7:
                                print(f"{trace_j}: not pickable, cc {ccf_data.max()}")
                                give_up += 1
                                if give_up > 10:
                                    break
                            lmax = hypermax(ccf_lagtime, ccf_data)

                            self.del_pick(trace_j.timepick, trace_offset_j)
                            trace_j.__setattr__('timepick', timepick + lmax)
                            if self.verbose:
                                print(f"{trace_j}: pick extrapolated at {timepick + lmax:.9f}, cc {ccf_data.max()}")
                            self.add_pick(timepick + lmax, trace_offset_j)

        elif event.key == "u":
            self.remove_last_pick()

        elif event.key == "r":
            if input('remove all picks?') == "y":
                self.remove_all_picks()

        elif event.key in ['p']:
            _timepicks, _traceoffsets = self.get_picks()
            if len(_timepicks):
                for tt, pp in zip(_timepicks, _traceoffsets):
                    print(tt, pp)
            else:
                print('no picks')

        elif event.key in ['j']:
            _timepicks, _traceoffsets = self.get_picks()
            if len(_timepicks):
                outputfilename = "_picks.csv"
                with open(outputfilename, 'w') as fid:
                    fid.write('#timepick_sec, traceoffset\n')
                    for tt, pp in zip(*self.get_picks()):
                        fid.write(f'{tt}, {pp}\n')
                print(f'{outputfilename} saved.')
            else:
                print('no picks')

        elif event.key in ['o']:
            if self.save_stream_as is None:
                print('option o not available (specify a filename with save_stream_as)')
            else:
                _timepicks, _traceoffsets = self.get_picks()

                # save stream to save_stream_as
                # WARNING : MAY REMOVE ADDITIONAL KEYS THAT ARE NOT LOADED IN SELF.STREAM!
                self.stream.to_npz(self.save_stream_as, additional_keys="*")
                print(f'{self.save_stream_as} saved.')
            
        self.refresh()

    def remove_last_pick(self):
        if len(self.pick_line_handles):
            if self.swapxy:
                (trace_offset,), _ = self.pick_line_handles[-1].get_data()
            else:
                _, (trace_offset,) = self.pick_line_handles[-1].get_data()

            for n in range(len(self.stream)):
                if np.isclose(self.trace_offsets[n], trace_offset):
                    self.stream[n].timepick = DEFAULT_TIMEPICK
                    if self.verbose:
                        print(f"{self.stream[n]}: remove pick")

            self.pick_line_handles.pop(-1).remove()
            self.pick_text_handles.pop(-1).remove()

    def remove_all_picks(self):
        self.stream.set('timepick', DEFAULT_TIMEPICK * np.ones(len(self.stream)))

        while len(self.pick_line_handles):
            self.pick_line_handles.pop(-1).remove()

        while len(self.pick_text_handles):
            self.pick_text_handles.pop(-1).remove()

    def add_pick(self, timepick, trace_offset):
        # print('**add', timepick, trace_offset)
        # hdl, = event.inaxes.plot([timepick, timepick], [traceindex - 0.5, traceindex + 0.5], 'r')
        if self.swapxy:
            hdl, = self.ax.plot([trace_offset], [timepick], 'r_')  # [timepick, timepick], [traceindex - 0.5, traceindex + 0.5], 'r')
        else:
            hdl, = self.ax.plot([timepick], [trace_offset], 'r|')  # [timepick, timepick], [traceindex - 0.5, traceindex + 0.5], 'r')
        self.pick_line_handles.append(hdl)

        if self.swapxy:
            hdl = self.ax.text(trace_offset, timepick, '', color="r", horizontalalignment="left")
        else:
            # hdl = event.inaxes.text(timepick, traceindex + 0.5, timepick, color="r", horizontalalignment="right")
            # hdl = self.ax.text(timepick, traceindex + 0.5, timepick, color="r", horizontalalignment="right")
            # hdl = self.ax.text(timepick, trace_offset, timepick, color="r", horizontalalignment="right")
            hdl = self.ax.text(timepick, trace_offset, '', color="r", horizontalalignment="right")
        self.pick_text_handles.append(hdl)

    def del_pick(self, timepick, trace_offset):
    
        keep_list = []
        for n, (hdl, thdl) in enumerate(zip(self.pick_line_handles, self.pick_text_handles)):

            if self.swapxy:
                (_trace_offset, ), (_timepick, ) = hdl.get_data()
            else:
                (_timepick, ), (_trace_offset, ) = hdl.get_data()

            if np.isclose(trace_offset, _trace_offset) and np.isclose(timepick, _timepick):
                hdl.remove()
                thdl.remove()
            else:
                keep_list.append(n)

        self.pick_line_handles = [self.pick_line_handles[_] for _ in keep_list]
        self.pick_text_handles = [self.pick_text_handles[_] for _ in keep_list]

    def refresh(self):
        # self.ax.figure.canvas.restore_region(self.background)
        for _ in self.pick_line_handles:
            self.ax.draw_artist(_)
        for _ in self.pick_text_handles:
            self.ax.draw_artist(_)
        self.ax.figure.canvas.blit(self.ax.bbox)

    def get_picks(self):
        timepicks, traceoffsets = [], []
        for hdl in self.pick_line_handles:
            if self.swapxy:
                traceoffset, timepick = hdl.get_data()
            else:
                timepick, traceoffset = hdl.get_data()
            timepicks.append(timepick[0])
            traceoffsets.append(traceoffset[0])
        return timepicks, traceoffsets


# def set_picker(ax, verbose: bool=True) -> Picker:
#     picker = Picker(ax, verbose)
#     ax.figure.canvas.mpl_connect('key_press_event', picker)
#     return picker
