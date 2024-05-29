from math import pi
import numpy as np

from .gate import Gate


class TGate(Gate):
    """
    Single qubit T gate
    """
    _array = np.array([[1, 0], [0, np.exp(1j * pi / 4)]], dtype=np.complex128)

    def __init__(self):
        """
        Create new T gate.
        """
        super().__init__(name='t', num_qubits=1, params=[])


class TdGate(Gate):
    """
    Single qubit T-dagger gate
    """
    _array = np.array([[1, 0], [0, np.exp(-1j * pi / 4)]], dtype=np.complex128)

    def __init__(self):
        """
        Create new TD gate.
        """
        super().__init__(name='td', num_qubits=1, params=[])
