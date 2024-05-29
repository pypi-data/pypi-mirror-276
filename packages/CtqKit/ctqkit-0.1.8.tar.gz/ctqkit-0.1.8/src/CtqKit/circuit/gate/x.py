import numpy as np

from .gate import Gate


class XGate(Gate):
    """
    The single-qubit Pauli-X gate
    """
    _array = np.array([[0, 1], [1, 0]], dtype=np.complex128)

    def __init__(self):
        """
        Create new X gate.
        """
        super().__init__(name='x', num_qubits=1, params=[])
