"""Circuitos cuanticos de referencia."""

from __future__ import annotations

import numpy as np

from quantum_circuits.circuit import QuantumCircuit


def superposition(qubits: int = 1) -> QuantumCircuit:
    """Crea una superposicion uniforme sobre todos los qubits."""
    circuit = QuantumCircuit(qubits)
    for qubit in range(qubits):
        circuit.h(qubit)
    return circuit


def bell_state() -> QuantumCircuit:
    """Prepara el estado entrelazado (|00> + |11>) / sqrt(2)."""
    return QuantumCircuit(2).h(0).cnot(0, 1)


def teleportation(alpha: complex = 1, beta: complex = 0) -> QuantumCircuit:
    """Construye la parte unitaria del protocolo de teleportacion cuantica.

    El qubit 0 contiene el estado a teleportar, y los qubits 1 y 2 forman el
    par de Bell compartido. La medicion y correccion clasica se estudian por
    separado porque son probabilisticas.
    """
    initial = np.zeros(8, dtype=complex)
    initial[0] = alpha
    initial[4] = beta
    circuit = QuantumCircuit(3, initial)
    circuit.h(1).cnot(1, 2)
    circuit.cnot(0, 1).h(0)
    return circuit


def deutsch_jozsa(kind: str = "balanced") -> QuantumCircuit:
    """Circuito Deutsch-Jozsa para una funcion de 1 bit.

    ``kind="constant"`` usa f(x)=0. ``kind="balanced"`` usa f(x)=x.
    """
    if kind not in {"constant", "balanced"}:
        raise ValueError("kind debe ser 'constant' o 'balanced'.")

    circuit = QuantumCircuit(2)
    circuit.x(1)
    circuit.h(0).h(1)
    if kind == "balanced":
        circuit.cnot(0, 1)
    circuit.h(0)
    return circuit


def grover_2qubits(marked: str = "11") -> QuantumCircuit:
    """Grover sobre 2 qubits con un estado marcado."""
    if len(marked) != 2 or any(bit not in "01" for bit in marked):
        raise ValueError("marked debe ser una cadena binaria de 2 bits, por ejemplo '11'.")

    circuit = superposition(2)
    circuit.oracle_phase_flip([marked])

    # Difusor: H^n X^n CZ X^n H^n.
    for qubit in range(2):
        circuit.h(qubit).x(qubit)
    circuit.cz(0, 1)
    for qubit in range(2):
        circuit.x(qubit).h(qubit)
    return circuit


def qft(qubits: int, basis_state: int = 1) -> QuantumCircuit:
    """Transformada Cuantica de Fourier sobre un estado base."""
    if not 0 <= basis_state < 2**qubits:
        raise ValueError("basis_state fuera de rango.")

    state = np.zeros(2**qubits, dtype=complex)
    state[basis_state] = 1
    circuit = QuantumCircuit(qubits, state)

    for target in range(qubits):
        circuit.h(target)
        for control in range(target + 1, qubits):
            angle = np.pi / (2 ** (control - target))
            circuit.controlled_phase(control, target, angle)

    for qubit in range(qubits // 2):
        circuit.swap(qubit, qubits - qubit - 1)
    return circuit

