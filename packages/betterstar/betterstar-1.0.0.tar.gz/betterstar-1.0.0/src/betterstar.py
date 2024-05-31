import math
import numpy as np
from matplotlib.path import Path

s2 = math.sqrt(2) / 2
# Define the marker shape
verts = np.array(
    [[-1, 0], [1, 0], [0, 1], [0, -1], [s2, s2], [-s2, -s2], [-s2, s2], [s2, -s2]]
)
codes = [
    Path.MOVETO,
    Path.LINETO,
    Path.MOVETO,
    Path.LINETO,
    Path.MOVETO,
    Path.LINETO,
    Path.MOVETO,
    Path.LINETO,
]
star = Path(verts, codes)
