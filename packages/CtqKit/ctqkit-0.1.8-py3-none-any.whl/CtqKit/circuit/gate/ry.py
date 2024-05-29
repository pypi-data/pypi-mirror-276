from math import cos, sin

import numpy as np

from .gate import Gate


class RyGate(Gate):
    """
    Single-qubit rotation about the Y axis.
    """

    def __init__(self, theta: float):
        """
        Create new RY gate.
        """
        super().__init__(name='ry', num_qubits=1, params=[theta])

    def __array__(self, dtype=None):
        """Return a numpy.array for the RY gate."""
        c = cos(self.params[0] / 2)
        s = sin(self.params[0] / 2)
        return np.array([[c, - s], [s, c]], dtype=dtype)
