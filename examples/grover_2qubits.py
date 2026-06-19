from quantum_circuits import grover_2qubits
from quantum_circuits.visualization import plot_probabilities


def main() -> None:
    circuit = grover_2qubits(marked="10")
    probabilities = circuit.probabilities()

    print("Operaciones:", " -> ".join(circuit.operations))
    print("Probabilidades:", probabilities)
    print("Muestras:", circuit.sample(shots=1000, seed=123))

    plot_probabilities(probabilities, "Grover 2 qubits: estado marcado |10>", "outputs/grover.png")


if __name__ == "__main__":
    main()

