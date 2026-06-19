"""Simulador didactico de circuitos cuanticos basado en vectores de estado."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import numpy as np

from quantum_circuits import gates


def _basis_label(index: int, qubits: int) -> str:
    return format(index, f"0{qubits}b")


@dataclass
class QuantumCircuit:
    """Circuito cuantico pequeno para aprendizaje.

    La convencion usada es big-endian: el qubit 0 corresponde al bit mas
    significativo en etiquetas como ``|010>``.
    """

    qubits: int
    state: np.ndarray | None = None
    operations: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.qubits < 1:
            raise ValueError("El circuito necesita al menos un qubit.")

        dimension = 2**self.qubits
        if self.state is None:
            self.state = np.zeros(dimension, dtype=complex)
            self.state[0] = 1.0
            return

        self.state = np.asarray(self.state, dtype=complex)
        if self.state.shape != (dimension,):
            raise ValueError(f"El estado debe tener dimension {dimension}.")
        self._normalize()

    def copy(self) -> "QuantumCircuit":
        return QuantumCircuit(self.qubits, self.state.copy(), self.operations.copy())

    def amplitudes(self, decimals: int = 6) -> dict[str, complex]:
        return {
            _basis_label(i, self.qubits): np.round(amplitude, decimals)
            for i, amplitude in enumerate(self.state)
            if not np.isclose(amplitude, 0)
        }

    def probabilities(self, decimals: int = 6) -> dict[str, float]:
        return {
            _basis_label(i, self.qubits): round(float(abs(amplitude) ** 2), decimals)
            for i, amplitude in enumerate(self.state)
            if not np.isclose(abs(amplitude) ** 2, 0)
        }

    def sample(self, shots: int = 1024, seed: int | None = None) -> dict[str, int]:
        if shots < 1:
            raise ValueError("shots debe ser positivo.")

        rng = np.random.default_rng(seed)
        probabilities = np.abs(self.state) ** 2
        outcomes = rng.choice(len(probabilities), size=shots, p=probabilities)
        counts: dict[str, int] = {}
        for outcome in outcomes:
            label = _basis_label(int(outcome), self.qubits)
            counts[label] = counts.get(label, 0) + 1
        return dict(sorted(counts.items()))

    def apply(self, matrix: np.ndarray, target: int, label: str | None = None) -> "QuantumCircuit":
        self._validate_qubit(target)
        self._validate_single_qubit_gate(matrix)

        tensor = self.state.reshape([2] * self.qubits)
        tensor = np.moveaxis(tensor, target, 0)
        tensor = np.tensordot(matrix, tensor, axes=([1], [0]))
        tensor = np.moveaxis(tensor, 0, target)
        self.state = tensor.reshape(-1)

        self.operations.append(label or f"U({target})")
        return self

    def controlled(
        self,
        matrix: np.ndarray,
        control: int,
        target: int,
        label: str | None = None,
    ) -> "QuantumCircuit":
        self._validate_qubit(control)
        self._validate_qubit(target)
        self._validate_single_qubit_gate(matrix)
        if control == target:
            raise ValueError("control y target deben ser qubits distintos.")

        new_state = self.state.copy()
        for index, amplitude in enumerate(self.state):
            if self._bit(index, control) == 1 and self._bit(index, target) == 0:
                paired = self._flip_bit(index, target)
                vector = np.array([self.state[index], self.state[paired]], dtype=complex)
                updated = matrix @ vector
                new_state[index], new_state[paired] = updated[0], updated[1]

        self.state = new_state
        self.operations.append(label or f"CU({control}->{target})")
        return self

    def swap(self, a: int, b: int) -> "QuantumCircuit":
        self._validate_qubit(a)
        self._validate_qubit(b)
        if a == b:
            return self

        new_state = self.state.copy()
        for index, amplitude in enumerate(self.state):
            bit_a = self._bit(index, a)
            bit_b = self._bit(index, b)
            if bit_a != bit_b:
                swapped = self._flip_bit(self._flip_bit(index, a), b)
                new_state[swapped] = amplitude
        self.state = new_state
        self.operations.append(f"SWAP({a},{b})")
        return self

    def measure(self, target: int, seed: int | None = None) -> tuple[int, "QuantumCircuit"]:
        self._validate_qubit(target)
        probability_one = sum(
            abs(amplitude) ** 2
            for index, amplitude in enumerate(self.state)
            if self._bit(index, target) == 1
        )
        rng = np.random.default_rng(seed)
        result = int(rng.random() < probability_one)

        for index in range(len(self.state)):
            if self._bit(index, target) != result:
                self.state[index] = 0

        self._normalize()
        self.operations.append(f"M({target})={result}")
        return result, self

    def h(self, target: int) -> "QuantumCircuit":
        return self.apply(gates.H, target, f"H({target})")

    def x(self, target: int) -> "QuantumCircuit":
        return self.apply(gates.X, target, f"X({target})")

    def y(self, target: int) -> "QuantumCircuit":
        return self.apply(gates.Y, target, f"Y({target})")

    def z(self, target: int) -> "QuantumCircuit":
        return self.apply(gates.Z, target, f"Z({target})")

    def s(self, target: int) -> "QuantumCircuit":
        return self.apply(gates.S, target, f"S({target})")

    def t(self, target: int) -> "QuantumCircuit":
        return self.apply(gates.T, target, f"T({target})")

    def rx(self, target: int, theta: float) -> "QuantumCircuit":
        return self.apply(gates.rx(theta), target, f"RX({target},{theta:.3f})")

    def ry(self, target: int, theta: float) -> "QuantumCircuit":
        return self.apply(gates.ry(theta), target, f"RY({target},{theta:.3f})")

    def rz(self, target: int, theta: float) -> "QuantumCircuit":
        return self.apply(gates.rz(theta), target, f"RZ({target},{theta:.3f})")

    def phase(self, target: int, theta: float) -> "QuantumCircuit":
        return self.apply(gates.phase(theta), target, f"P({target},{theta:.3f})")

    def cnot(self, control: int, target: int) -> "QuantumCircuit":
        return self.controlled(gates.X, control, target, f"CNOT({control}->{target})")

    def cz(self, control: int, target: int) -> "QuantumCircuit":
        return self.controlled(gates.Z, control, target, f"CZ({control}->{target})")

    def controlled_phase(self, control: int, target: int, theta: float) -> "QuantumCircuit":
        return self.controlled(gates.phase(theta), control, target, f"CP({control}->{target})")

    def oracle_phase_flip(self, marked_states: Iterable[str]) -> "QuantumCircuit":
        marked = set(marked_states)
        for label in marked:
            if len(label) != self.qubits or any(bit not in "01" for bit in label):
                raise ValueError(f"Estado marcado invalido: {label!r}")

        for index in range(len(self.state)):
            if _basis_label(index, self.qubits) in marked:
                self.state[index] *= -1
        self.operations.append(f"Oracle({','.join(sorted(marked))})")
        return self

    def _normalize(self) -> None:
        norm = np.linalg.norm(self.state)
        if np.isclose(norm, 0):
            raise ValueError("El estado no puede tener norma cero.")
        self.state = self.state / norm

    def _validate_qubit(self, qubit: int) -> None:
        if not 0 <= qubit < self.qubits:
            raise IndexError(f"Qubit fuera de rango: {qubit}.")

    @staticmethod
    def _validate_single_qubit_gate(matrix: np.ndarray) -> None:
        matrix = np.asarray(matrix, dtype=complex)
        if matrix.shape != (2, 2):
            raise ValueError("La compuerta debe ser una matriz 2x2.")

    def _bit(self, index: int, qubit: int) -> int:
        shift = self.qubits - qubit - 1
        return (index >> shift) & 1

    def _flip_bit(self, index: int, qubit: int) -> int:
        shift = self.qubits - qubit - 1
        return index ^ (1 << shift)

