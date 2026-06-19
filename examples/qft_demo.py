from quantum_circuits import qft


def main() -> None:
    circuit = qft(qubits=3, basis_state=1)

    print("Operaciones:", " -> ".join(circuit.operations))
    print("Amplitudes no nulas:")
    for state, amplitude in circuit.amplitudes(decimals=4).items():
        print(f"|{state}>: {amplitude}")


if __name__ == "__main__":
    main()

