from __future__ import annotations

import numpy as np

ComplexMatrix = np.ndarray

IDENTITY: ComplexMatrix = np.array([[1, 0], [0, 1]], dtype=complex)
X: ComplexMatrix = np.array([[0, 1], [1, 0]], dtype=complex)
Y: ComplexMatrix = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z: ComplexMatrix = np.array([[1, 0], [0, -1]], dtype=complex)
H: ComplexMatrix = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
S: ComplexMatrix = np.array([[1, 0], [0, 1j]], dtype=complex)
T: ComplexMatrix = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)


def rx(theta: float) -> ComplexMatrix:
    return np.array(
        [
            [np.cos(theta / 2), -1j * np.sin(theta / 2)],
            [-1j * np.sin(theta / 2), np.cos(theta / 2)],
        ],
        dtype=complex,
    )


def ry(theta: float) -> ComplexMatrix:
    return np.array(
        [
            [np.cos(theta / 2), -np.sin(theta / 2)],
            [np.sin(theta / 2), np.cos(theta / 2)],
        ],
        dtype=complex,
    )


def rz(theta: float) -> ComplexMatrix:
    return np.array(
        [
            [np.exp(-1j * theta / 2), 0],
            [0, np.exp(1j * theta / 2)],
        ],
        dtype=complex,
    )


def phase(theta: float) -> ComplexMatrix:
    return np.array([[1, 0], [0, np.exp(1j * theta)]], dtype=complex)
