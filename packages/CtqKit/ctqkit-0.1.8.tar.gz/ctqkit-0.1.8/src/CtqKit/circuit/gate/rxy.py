from math import cos, sin

import numpy as np

from .gate import Gate


class RxyGate(Gate):
    """
    Single-qubit rotation about the XY plane.
    """

    def __init__(self, phi: float, theta: float):
        """
        Create new RXY gate.
        """
        super().__init__(name='rxy', num_qubits=1, params=[phi, theta])

    def __array__(self, dtype=None):
        """Return a numpy.array for the RXY gate."""
        phi, theta = self.params
        c = cos(theta / 2)
        s = sin(theta / 2)
        return np.array([
            [c, -1j * np.exp(-1j * phi) * s],
            [-1j * np.exp(1j * phi) * s, c]
        ], dtype=dtype)
