"""
Semplice script per leggere consumi energetici di inferenze LLM da CSV
e produrre alcuni grafici con seaborn.

Uso:
  python scripts/plot_energy.py

Lo script cerca il file recordings/llm_energy_test.csv. Se non esiste,
stampa un messaggio d'errore. Salva i plot in recordings/plots/.
"""
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / "recordings" / "llm_energy_test.csv"
    out_dir = repo_root / "recordings" / "plots"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        print(f"File CSV non trovato: {csv_path}")
        print("Creane uno nella cartella recordings o usa uno script per generarne uno di test.")
        return

    df = pd.read_csv(csv_path, parse_dates=["timestamp"]) 
    sns.set_theme(style="darkgrid")

    # Grafico 1: energia (joules) nel tempo con seaborn lineplot
    plt.figure(figsize=(10, 4))
    sns.lineplot(x="timestamp", y="energy_joules", data=df, marker="o")
    plt.xlabel("Timestamp")
    plt.ylabel("Energy (J)")
    plt.title("Energy per inference over time")
    plt.tight_layout()
    plt.savefig(out_dir / "energy_time_series.png")
    plt.close()

    # Grafico 2: histogram energia con seaborn
    plt.figure(figsize=(6, 4))
    sns.histplot(data=df, x="energy_joules", bins=12, kde=True)
    plt.xlabel("Energy (J)")
    plt.ylabel("Count")
    plt.title("Energy distribution")
    plt.tight_layout()
    plt.savefig(out_dir / "energy_histogram.png")
    plt.close()

    # Grafico 3: boxplot per modello
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df, x="model", y="energy_joules")
    plt.xlabel("Model")
    plt.ylabel("Energy (J)")
    plt.title("Energy by model")
    plt.tight_layout()
    plt.savefig(out_dir / "energy_by_model.png")
    plt.close()

    # Grafico 4: scatter duration vs energy con regressione
    plt.figure(figsize=(6, 4))
    sns.scatterplot(data=df, x="duration_ms", y="energy_joules", hue="model", s=100, alpha=0.7)
    plt.xlabel("Duration (ms)")
    plt.ylabel("Energy (J)")
    plt.title("Duration vs Energy")
    plt.tight_layout()
    plt.savefig(out_dir / "duration_vs_energy.png")
    plt.close()

    print(f"Plots salvati in: {out_dir}")


if __name__ == "__main__":
    main()
