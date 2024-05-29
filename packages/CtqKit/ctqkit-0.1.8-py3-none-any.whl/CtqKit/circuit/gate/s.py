import numpy as np

from .gate import Gate


class SGate(Gate):
    """
    Single qubit S gate
    """
    _array = np.array([[1, 0], [0, 1j]], dtype=np.complex128)

    def __init__(self):
        """
        Create new S gate.
        """
        super().__init__(name='s', num_qubits=1, params=[])


class SdGate(Gate):
    """
    Single qubit S-dagger gate
    """
    _array = np.array([[1, 0], [0, -1j]], dtype=np.complex128)

    def __init__(self):
        """
        Create new SD gate.
        """
        super().__init__(name='sd', num_qubits=1, params=[])
