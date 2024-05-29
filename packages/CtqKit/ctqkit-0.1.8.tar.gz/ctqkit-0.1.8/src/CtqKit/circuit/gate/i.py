from math import sqrt

import numpy as np

from .gate import Gate


class IGate(Gate):
    """
    Identity gate.
    """
    _array = np.array([[1, 0], [0, 1]], dtype=np.complex128)

    def __init__(self, t: int):
        """
        Create new I gate.
        :param t: time to wait, unit is 0.5ns
        """
        super().__init__(name='i', num_qubits=1, params=[])
