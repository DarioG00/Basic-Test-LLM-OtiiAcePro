# BasicTestLLM

Repository di test per eseguire inferenze con `llama.cpp` su un Raspberry Pi via SSH usando Python.

## Struttura del progetto

- `LLM_inference_test.py` - script principale che si connette in SSH al Raspberry Pi, avvia `llama.cpp` in modalità interattiva e invia i prompt uno alla volta.
- `config.json` - file di configurazione con parametri SSH e `llama.cpp`:
  - `host`, `username`, `password`
  - `llama_cpp_dir`, `llama_bin`, `model_path`, `threads`
  - `prompts`
- `otii_connection_test.py` - test di connessione TCP minimale a Otii Server.

## Requisiti

- Python 3.8+ (consigliato Python 3.10+)
- `paramiko`
- `json` (modulo standard)

## Installazione

1. Crea e attiva un ambiente virtuale (opzionale ma consigliato):

```bash
python -m venv env
source env/bin/activate      # Linux/macOS
env\Scripts\activate       # Windows
```

2. Installa le dipendenze:

```bash
python -m pip install -r requirements.txt
```

## Configurazione

Modifica `config.json` con i valori corretti per la tua configurazione SSH e il percorso del modello:

```json
{
  "host": "192.168.121.175",
  "username": "dario",
  "password": "Tes1&2026",
  "llama_cpp_dir": "./llama.cpp",
  "llama_bin": "./build/bin/llama-cli",
  "model_path": "./LLMs/gemma-2-2b-it-Q4_K_M.gguf",
  "threads": 4,
  "prompts": [
    "Explain quantum mechanics in one sentence.",
    "Write a haiku about Linux.",
    "What is the capital of Japan?"
  ]
}
```

## Uso

Esegui lo script principale:

```bash
python LLM_inference_test.py
```

Lo script:

- si connette via SSH al Raspberry Pi
- lancia `llama.cpp` con il modello specificato
- attende il prompt `>` per verificare che il modello sia pronto
- invia ogni prompt a `llama.cpp` uno alla volta
- legge e mostra l'output e le metriche di throughput

## Note

- Se il prompt `>` non viene rilevato entro il timeout, lo script prosegue comunque.
- `config.json` contiene dati sensibili: evita di committarlo su repository pubblici.

## Commit suggerito

`aggiorna README con istruzioni coerenti per LLM_inference_test e configurazione JSON`
