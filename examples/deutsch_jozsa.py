from quantum_circuits import deutsch_jozsa


def main() -> None:
    for kind in ("constant", "balanced"):
        circuit = deutsch_jozsa(kind)
        print(f"\nFuncion {kind}")
        print("Operaciones:", " -> ".join(circuit.operations))
        print("Probabilidades:", circuit.probabilities())


if __name__ == "__main__":
    main()

