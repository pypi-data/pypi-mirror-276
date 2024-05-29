from .instruction import Instruction


class Measure(Instruction):
    """
    Measure Qubit Instruction
    """

    def __init__(self, num_qubits: int):
        """
        Create new measure instruction.
        """
        self._name = 'm'
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
