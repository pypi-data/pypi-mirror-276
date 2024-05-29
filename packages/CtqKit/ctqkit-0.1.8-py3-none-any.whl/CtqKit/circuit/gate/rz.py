from math import cos, sin

import numpy as np

from .gate import Gate


class RzGate(Gate):
    """
    Single-qubit rotation about the Z axis.
    """

    def __init__(self, theta: float):
        """
        Create new RZ gate.
        """
        super().__init__(name='rz', num_qubits=1, params=[theta])

    def __array__(self, dtype=None):
        """Return a numpy.array for the RZ gate."""
        theta = self.params[0]
        return np.array([
            [np.exp(-1j * theta / 2), 0],
            [0, np.exp(1j * theta / 2)]
        ], dtype=dtype)
