import numpy as np

from .gate import Gate


class YGate(Gate):
    """
    The single-qubit Pauli-Y gate
    """
    _array = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)

    def __init__(self):
        """
        Create new Y gate.
        """
        super().__init__(name='y', num_qubits=1, params=[])
