"""
Semplice script per leggere consumi energetici di inferenze LLM da CSV
e produrre alcuni grafici con pandas + matplotlib.

Uso:
  python scripts/plot_energy.py

Lo script cerca il file recordings/llm_energy_test.csv. Se non esiste,
stampa un messaggio d'errore. Salva i plot in recordings/plots/.
"""
from pathlib import Path
import pandas as pd
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

    # Grafico 1: energia (joules) nel tempo
    plt.figure(figsize=(10, 4))
    plt.plot(df["timestamp"], df["energy_joules"], marker="o", linestyle="-")
    plt.xlabel("Timestamp")
    plt.ylabel("Energy (J)")
    plt.title("Energy per inference over time")
    plt.tight_layout()
    plt.savefig(out_dir / "energy_time_series.png")
    plt.close()

    # Grafico 2: histogram energia
    plt.figure(figsize=(6, 4))
    plt.hist(df["energy_joules"], bins=12)
    plt.xlabel("Energy (J)")
    plt.ylabel("Count")
    plt.title("Energy distribution")
    plt.tight_layout()
    plt.savefig(out_dir / "energy_histogram.png")
    plt.close()

    # Grafico 3: boxplot per modello
    plt.figure(figsize=(6, 4))
    df.boxplot(column="energy_joules", by="model")
    plt.xlabel("Model")
    plt.ylabel("Energy (J)")
    plt.title("Energy by model")
    plt.suptitle("")
    plt.tight_layout()
    plt.savefig(out_dir / "energy_by_model.png")
    plt.close()

    # Grafico 4: scatter duration vs energy
    plt.figure(figsize=(6, 4))
    plt.scatter(df["duration_ms"], df["energy_joules"], alpha=0.7)
    plt.xlabel("Duration (ms)")
    plt.ylabel("Energy (J)")
    plt.title("Duration vs Energy")
    plt.tight_layout()
    plt.savefig(out_dir / "duration_vs_energy.png")
    plt.close()

    print(f"Plots salvati in: {out_dir}")


if __name__ == "__main__":
    main()
