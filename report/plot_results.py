from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt


def plot_results(results: Dict[str, dict], output_path: str = "comparison.png"):
    names = list(results.keys())
    runtime = [results[n]["runtime"] for n in names]
    cost = [results[n]["cost"] for n in names]
    explored = [results[n]["explored"] for n in names]
    path_len = [results[n]["path_len"] for n in names]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes[0, 0].bar(names, runtime)
    axes[0, 0].set_title("Runtime (s)")
    axes[0, 1].bar(names, cost)
    axes[0, 1].set_title("Path Cost")
    axes[1, 0].bar(names, explored)
    axes[1, 0].set_title("Explored Nodes")
    axes[1, 1].bar(names, path_len)
    axes[1, 1].set_title("Path Length")

    for ax in axes.flat:
        ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
