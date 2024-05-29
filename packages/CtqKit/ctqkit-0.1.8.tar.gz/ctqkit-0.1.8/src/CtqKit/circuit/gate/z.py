import numpy as np

from .gate import Gate


class ZGate(Gate):
    """
    The single-qubit Pauli-Z gate
    """
    _array = np.array([[0, 1], [0, -1]], dtype=np.complex128)

    def __init__(self):
        """
        Create new Z gate.
        """
        super().__init__(name='z', num_qubits=1, params=[])


class CZGate(Gate):
    """
    Controlled-Z gate.
    """
    _array = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1],
    ], dtype=np.complex128)

    def __init__(self):
        """
        Create new CZ gate.
        """
        super().__init__(name='cz', num_qubits=2, params=[])
