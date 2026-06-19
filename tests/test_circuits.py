import numpy as np

from quantum_circuits import QuantumCircuit, bell_state, deutsch_jozsa, grover_2qubits, qft


def test_h_gate_creates_equal_superposition() -> None:
    circuit = QuantumCircuit(1).h(0)
    assert circuit.probabilities() == {"0": 0.5, "1": 0.5}


def test_bell_state_has_only_correlated_outcomes() -> None:
    circuit = bell_state()
    assert circuit.probabilities() == {"00": 0.5, "11": 0.5}


def test_deutsch_jozsa_constant_vs_balanced() -> None:
    assert deutsch_jozsa("constant").probabilities() == {"00": 0.5, "01": 0.5}
    assert deutsch_jozsa("balanced").probabilities() == {"10": 0.5, "11": 0.5}


def test_grover_finds_marked_state_for_two_qubits() -> None:
    circuit = grover_2qubits("10")
    assert circuit.probabilities() == {"10": 1.0}


def test_qft_preserves_norm() -> None:
    circuit = qft(3, basis_state=1)
    assert np.isclose(np.linalg.norm(circuit.state), 1)
