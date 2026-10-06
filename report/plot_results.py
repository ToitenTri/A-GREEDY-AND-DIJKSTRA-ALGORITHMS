from math import isfinite
from pathlib import Path

import matplotlib.pyplot as plt


def plot_results(results: dict[str, dict], output_path: str = "comparison.png"):
    names = list(results)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    metrics = (("runtime", "Search time (s)"), ("cost", "Path Cost"),
               ("explored", "Explored Nodes"), ("path_len", "Path Length"))
    for ax, (key, title) in zip(axes.flat, metrics):
        values = [results[name][key] for name in names]
        # Plot missing paths as gaps with an explicit N/A annotation.
        bars = ax.bar(names, [value if isfinite(value) else float("nan") for value in values])
        ax.set_xlim(-0.5, len(names) - 0.5)
        for bar, value in zip(bars, values):
            if not isfinite(value):
                ax.text(bar.get_x() + bar.get_width()/2, 0, "N/A", ha="center", va="bottom",
                        transform=ax.get_xaxis_transform())
        if not any(isfinite(value) for value in values):
            ax.set_ylim(0, 1)
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=150)
    plt.close(fig)
