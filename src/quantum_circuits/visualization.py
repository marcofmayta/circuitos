from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def plot_probabilities(
    probabilities: dict[str, float],
    title: str = "Distribucion de probabilidades",
    output: str | Path | None = None,
) -> None:
    labels = list(probabilities)
    values = [probabilities[label] for label in labels]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(labels, values, color="#2f80ed")
    ax.set_ylim(0, 1)
    ax.set_xlabel("Estado base")
    ax.set_ylabel("Probabilidad")
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()

    if output is None:
        plt.show()
    else:
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=160)
        plt.close(fig)

