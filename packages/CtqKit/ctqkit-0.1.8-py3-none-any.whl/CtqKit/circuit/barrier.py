from .instruction import Instruction


class Barrier(Instruction):
    """
    Barrier instruction.
    """

    def __init__(self, num_qubits: int):
        """
        Create new barrier instruction.
        """
        self._name = 'b'
        self._num_qubits = num_qubits

    @property
    def name(self):
        return self._name

    @property
    def num_qubits(self):
        return self._num_qubits

    @num_qubits.setter
    def num_qubits(self, num_qubits: str):
        self._num_qubits = num_qubits
