# BasicTestLLM

Progetto di test per eseguire inferenze LLM con `llama.cpp` su un Raspberry Pi via SSH, con supporto per il monitoraggio energetico tramite Otii.

## 📋 Descrizione del Progetto

Questo repository contiene script Python per:
1. Testare la connessione SSH a un Raspberry Pi
2. Eseguire inferenze LLM usando `llama.cpp` in modalità interattiva via SSH
3. Testare la connessione a un power monitor Otii per il monitoraggio dei consumi energetici

---

## 📁 Descrizione dei File

### `LLM_inference_test.py`
Script principale che automatizza le inferenze LLM su un Raspberry Pi remoto.

**Cosa fa:**
- Si connette al Raspberry Pi via SSH usando le credenziali da `config.json`
- Avvia `llama.cpp` in modalità interattiva
- Invia una serie di prompt predefiniti al modello LLM
- Cattura l'output dalla shell remota e ne estrae le metriche di performance:
  - **Prompt TPS** (token per secondo durante l'elaborazione del prompt)
  - **Generation TPS** (token per secondo durante la generazione del testo)
- Legge l'output fino al prompt successivo (">") prima di inviare il prossimo comando
- Gestisce timeout e errori di connessione

**Dipendenze:** paramiko, re, time, json

---

### `SSH_connection_test.py`
Script di test minimale per verificare la connessione SSH al Raspberry Pi.

**Cosa fa:**
- Carica le credenziali SSH dal file `config.json`
- Si connette al Raspberry Pi usando paramiko
- Esegue un comando di verifica remoto (echo di test)
- Stampa il risultato e chiude la connessione

**Utilità:** Utile per validare che le credenziali SSH e la raggiungibilità della macchina remota sono corrette prima di eseguire inferenze complesse.

**Dipendenze:** paramiko, json

---

### `otii_connection_test.py`
Script di test per verificare la connessione a un Otii Server (power monitor).

**Cosa fa:**
- Importa il client TCP dell'Otii
- Tenta di connettersi al server Otii
- Gestisce gli errori di licenza (comune nel test iniziale)
- Verifica se il dispositivo di monitoraggio energetico è raggiungibile

**Utilità:** Consente di verificare che il dispositivo Otii sia operativo e accessibile prima di eseguire test di consumo energetico.

**Dipendenze:** otii_tcp_client

---

### `config.json`
File di configurazione centralizzato che contiene tutti i parametri necessari per SSH e `llama.cpp`.

**Parametri:**
- **`host`**: Indirizzo IP del Raspberry Pi (es. 192.168.121.175). **Nota:** L'indirizzo IP non è statico ma assegnato dinamicamente dalla rete locale (DHCP). Verificare l'indirizzo corrente del dispositivo prima di ogni connessione.
- **`username`**: Nome utente SSH (es. dario)
- **`password`**: Password SSH
- **`llama_bin`**: Percorso relativo/assoluto dell'eseguibile llama-cli (es. `./llama.cpp/build/bin/llama-cli`)
- **`model_path`**: Percorso al modello GGUF (es. `./LLMs/gemma-2-2b-it-Q4_K_M.gguf`)
- **`threads`**: Numero di thread da usare per l'inferenza (es. 4)
- **`prompts`**: Array di stringhe contenenti i prompt da testare

**Formato:**
```json
{
  "host": "192.168.121.175",
  "username": "dario",
  "password": "password",
  "llama_bin": "./llama.cpp/build/bin/llama-cli",
  "model_path": "./LLMs/model.gguf",
  "threads": 4,
  "prompts": [
    "Explain quantum mechanics in one sentence.",
    "Write a haiku about Linux."
  ]
}
```

---

### `requirements.txt`
File che specifica tutte le dipendenze Python necessarie per eseguire gli script.

**Pacchetti principali:**
- **`paramiko`**: Client SSH per la connessione remota al Raspberry Pi
- **`otii_tcp_client`**: Client TCP per la connessione al dispositivo Otii
- **Dipendenze transitorie:** bcrypt, cffi, cryptography, pynacl (necessarie per paramiko)

**Utilizzo:**
```bash
pip install -r requirements.txt
```

---

## 🚀 Installazione e Setup

### 1. Ambiente Virtuale
```bash
python -m venv envTest
source envTest/bin/activate      # Linux/macOS
envTest\Scripts\activate          # Windows
```

### 2. Installare Dipendenze
```bash
pip install -r requirements.txt
```

### 3. Configurare `config.json`
Modifica il file con i tuoi parametri:
- IP e credenziali del Raspberry Pi
- Percorsi di llama.cpp e del modello
- I prompt da testare

---

## 🧪 Esecuzione degli Script

### Test SSH (consigliato prima)
```bash
python SSH_connection_test.py
```

### Test Otii (se hai il dispositivo)
```bash
python otii_connection_test.py
```

### Esecuzione Inferenze LLM
```bash
python LLM_inference_test.py
```

---

## ⚙️ Requisiti di Sistema

- Python 3.8+ (consigliato 3.10+)
- Accesso SSH a un Raspberry Pi con `llama.cpp` installato
- (Opzionale) Dispositivo Otii per il monitoraggio energetico

---

## 📝 Note

- I dati di configurazione sono centralizzati in `config.json` per facilitare le modifiche
- Lo script `LLM_inference_test.py` estrae automaticamente metriche di performance (TPS) dall'output di `llama.cpp`
- Il timeout di default per la lettura dell'output remoto è di 120 secondi (modificabile nel codice)
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
