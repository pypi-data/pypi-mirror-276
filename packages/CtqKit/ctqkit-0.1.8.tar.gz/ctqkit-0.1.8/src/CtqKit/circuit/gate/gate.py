import numpy as np

from src.CtqKit.circuit.instruction import Instruction


class Gate(Instruction):
    """
    quantum gate

    __array: numpy array
    """
    _array = None

    def __init__(self, name: str, num_qubits: int, params: list):
        """
        gate class constructor

        :param name: The name of the gate.
        :param num_qubits: The number of qubits the gate acts on.
        :param params: A list of parameters.
        """
        self._name = name
        self._num_qubits = num_qubits
        self._params = params

    def __array__(self, dtype=None):
        if dtype is None:
            dtype = np.float128
        return np.array(self._array, dtype=dtype)

    @property
    def name(self):
        """Return the name."""
        return self._name

    @name.setter
    def name(self, name):
        """Set the name."""
        self._name = name

    @property
    def params(self):
        """Return the params."""
        return self._params

    @params.setter
    def params(self, params):
        """Set the params."""
        self._params = params

    @property
    def num_qubits(self):
        """Return the params."""
        return self._num_qubits

    @num_qubits.setter
    def num_qubits(self, num_qubits):
        """Set the num_qubits."""
        self._num_qubits = num_qubits
