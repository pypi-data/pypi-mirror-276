from math import sqrt

import numpy as np

from .gate import Gate


class HGate(Gate):
    """
    Single-qubit Hadamard gate.
    """
    _array = 1 / sqrt(2) * np.array([[1, 1], [1, -1]], dtype=np.complex128)

    def __init__(self):
        """
        Create new H gate.
        """
        super().__init__(name='h', num_qubits=1, params=[])
