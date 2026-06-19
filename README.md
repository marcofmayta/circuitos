# Circuitos de Computacion Cuantica con Python

Proyecto didactico para estudiar circuitos cuanticos usando Python y NumPy. Incluye un simulador pequeno de vectores de estado, compuertas comunes, mediciones, visualizacion y ejemplos de algoritmos fundamentales.

## Contenido

- Estados de 1, 2 y n qubits.
- Compuertas `X`, `Y`, `Z`, `H`, `S`, `T`, rotaciones `RX`, `RY`, `RZ`.
- Compuertas controladas `CNOT`, `CZ`, `SWAP` y fase controlada.
- Mediciones probabilisticas y conteos tipo histograma.
- Circuitos y algoritmos:
  - Superposicion y medicion.
  - Estado de Bell.
  - Teleportacion cuantica.
  - Deutsch-Jozsa.
  - Grover para 2 qubits.
  - Transformada Cuantica de Fourier (QFT).
- Tutoriales en notebooks para usar el repositorio como material de clase.

## Instalacion

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Si solo quieres ejecutar los ejemplos:

```powershell
python -m pip install -r requirements.txt
```

## Uso rapido

```powershell
python examples\bell_state.py
python examples\grover_2qubits.py
python examples\qft_demo.py
```

## Ruta de notebooks

Los notebooks estan pensados como material progresivo:

1. `notebooks/00_fundamentos.ipynb`: qubits, amplitudes, probabilidades y medicion.
2. `notebooks/01_entrelazamiento_bell.ipynb`: estados de Bell y correlaciones.
3. `notebooks/02_oraculos_deutsch_grover.ipynb`: oraculos, Deutsch-Jozsa y Grover.
4. `notebooks/03_qft_teleportacion.ipynb`: QFT, fases y teleportacion.

Para abrirlos:

```powershell
python -m pip install -e ".[dev]"
jupyter notebook
```

Para validar que todos los notebooks ejecutan sin errores:

```powershell
python scripts\execute_notebooks.py
```

Tambien puedes usar el paquete desde Python:

```python
from quantum_circuits import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.cnot(0, 1)

print(qc.probabilities())
print(qc.sample(shots=1000, seed=7))
```

## Estructura

```text
src/quantum_circuits/
  circuit.py       # clase QuantumCircuit
  gates.py         # matrices de compuertas
  algorithms.py    # circuitos de algoritmos conocidos
  visualization.py # graficos de probabilidades
examples/          # scripts ejecutables
scripts/           # utilidades para validar material
tests/             # pruebas unitarias
notebooks/         # tutoriales ejecutables
.github/workflows/ # CI y CD para GitHub Actions
```

## Ejecutar pruebas

```powershell
pytest
```

## Idea del proyecto

El objetivo es que el codigo sea legible para aprender como se construyen los circuitos por debajo. No pretende reemplazar frameworks como Qiskit, Cirq o PennyLane; sirve como base educativa para entender la evolucion de estados, amplitudes, fases, entrelazamiento y medicion.
