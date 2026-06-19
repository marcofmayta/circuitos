from quantum_circuits import bell_state
from quantum_circuits.visualization import plot_probabilities


def main() -> None:
    circuit = bell_state()
    probabilities = circuit.probabilities()

    print("Operaciones:", " -> ".join(circuit.operations))
    print("Amplitudes:", circuit.amplitudes())
    print("Probabilidades:", probabilities)
    print("Muestras:", circuit.sample(shots=1000, seed=42))

    plot_probabilities(probabilities, "Estado de Bell", "outputs/bell_state.png")


if __name__ == "__main__":
    main()

