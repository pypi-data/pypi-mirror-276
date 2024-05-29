from abc import abstractmethod, ABC


class Instruction(ABC):
    """
    quantum instruction.

    All quantum operations are instructions,
    which are divided into three categories: Gate, Measure and Barrier.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def name(self):
        """Unique string identifier for operation type."""
        raise NotImplementedError

    @property
    @abstractmethod
    def num_qubits(self):
        """The number of qubits the gate acts on."""
        raise NotImplementedError
