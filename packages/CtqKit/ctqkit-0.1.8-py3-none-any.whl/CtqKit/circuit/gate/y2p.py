from math import sqrt
import numpy as np

from .gate import Gate


class Y2PGate(Gate):
    """
    The single-qubit gate, rotation around the y-axis of the Bloch sphere by 90 degrees
    """
    _array = 1 / sqrt(2) * np.array([[1, -1], [1, 1]], dtype=np.complex128)

    def __init__(self):
        """
        Create new Y2P gate.
        """
        super().__init__(name='y2p', num_qubits=1, params=[])
