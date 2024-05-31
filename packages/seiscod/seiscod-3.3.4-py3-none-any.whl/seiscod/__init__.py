import os
from seiscod.version import __version__
from seiscod.trace import Trace, FFTTrace
from seiscod.stream import Stream
from tempoo.timetick import timetick, microtimetick, millitimetick
from tempoo.utc import UTC, UTCFromTimestamp, UTCFromStr, UTCFromJulday

import numpy as np                # convenient
import matplotlib.pyplot as plt   # convenient

# the home directory of seiscod
__home__ = os.path.dirname(__file__)
