from typing import Union
import copy
import numpy as np


class RawTrace(object):
    """
    an basic object to store a trace header (builtin dictionnary) + numpy data array
    All reading tools should return a RawTrace or a list of RawTraces
    """
    def __init__(
            self,
            trace_dict: Union[None, dict] = None,
            trace_data: Union[None, list, np.ndarray] = None):
        if trace_dict is None:
            trace_dict = {}

        if trace_data is None:
            trace_data = np.array([], np.dtype('float64'))

        self.trace_dict = trace_dict
        self.trace_data = trace_data

    def copy(self):
        return copy.deepcopy(self)
