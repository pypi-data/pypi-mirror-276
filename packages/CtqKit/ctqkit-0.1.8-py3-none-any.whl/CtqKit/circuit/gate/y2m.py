from math import sqrt
import numpy as np

from .gate import Gate


class Y2MGate(Gate):
    """
    The single-qubit gate, rotation around the y-axis of the Bloch sphere by -pi/2 degrees
    """
    _array = 1 / sqrt(2) * np.array([[1, 1], [-1, 1]], dtype=np.complex128)

    def __init__(self):
        """
        Create new Y2M gate.
        """
        super().__init__(name='y2m', num_qubits=1, params=[])
