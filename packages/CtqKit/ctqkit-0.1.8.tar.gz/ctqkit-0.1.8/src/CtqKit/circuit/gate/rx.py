from math import cos, sin

import numpy as np

from .gate import Gate


class RxGate(Gate):
    """
    Single-qubit rotation about the X axis.
    """

    def __init__(self, theta: float):
        """
        Create new RX gate.
        """
        super().__init__(name='rx', num_qubits=1, params=[theta])

    def __array__(self, dtype=None):
        """Return a numpy.array for the RX gate."""
        c = cos(self.params[0] / 2)
        s = sin(self.params[0] / 2)
        return np.array([[c, -1j * s], [-1j * s, c]], dtype=dtype)
