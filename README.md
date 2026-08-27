# BasicTestLLM

Progetto di test per eseguire inferenze LLM con `llama.cpp` (versione b8989) su un Raspberry Pi via SSH, con supporto per il monitoraggio energetico tramite Otii.

# Nota fondamentale

I miei test di misurazione con Otii Ace Pro fallivano in quanto utilizzavo un cavo di alimentazione del Pi5 fatto a mano che univa i connettori a banana (lato Otii Ace Pro) con la parte di un cavo con connettore USB-C (quello di alimentazione del Pi5, appunto). Il cavo deve essere ufficiale perché all'accensione del Pi5, viene fatto un controllo automatico dei pin del connettore USB-C e se nota che manca il pin CC (Current Control) si spegne per protezione.

## 📋 Descrizione del Progetto

Questo repository contiene script Python per:
1. Testare la connessione SSH a un Raspberry Pi
2. Eseguire inferenze LLM usando `llama.cpp` via SSH
3. Testare la connessione a un power monitor Otii per il monitoraggio dei consumi energetici

---

## 📁 Struttura del repository

Questo progetto è organizzato in cartelle e file principali, ciascuno con uno scopo diverso.

### Sommario file e cartelle
| Percorso | Tipo | Descrizione |
|---|---|---|
| `README.md` | File | Documentazione del repository |
| `config.json` | File | Configurazione SSH, `llama.cpp`, modello e prompt |
| `requirements.txt` | File | Dipendenze Python necessarie |
| `envTest/` | Cartella | Ambiente virtuale Python con pacchetti installati |
| `recordings/` | Cartella | Dati e grafici dei test energetici |
| `scripts/` | Cartella | Script Python per test e inferenze |

### Dettaglio `scripts/`
| File | Descrizione |
|---|---|
| `LLM_inference_test.py` | Script principale per eseguire inferenze LLM su un Raspberry Pi remoto tramite SSH. Avvia `llama.cpp`, invia prompt e raccoglie metriche. |
| `SSH_connection_test.py` | Test minimale per convalidare la connessione SSH e verificare la raggiungibilità della macchina remota. |
| `otii_connection_test.py` | Test di connessione al server Otii TCP per validare il monitoraggio energetico. |
| `power_measurements_test.py` | Script di supporto per le misurazioni di potenza e la gestione dei dati Otii. |
| `plot_energy.py` | Genera grafici dai dati energetici contenuti in `recordings/llm_energy_test.csv`. |

### Dettaglio `recordings/`
| Percorso | Descrizione |
|---|---|
| `llm_energy_test.csv` | File CSV con le misurazioni energetiche raccolte durante i test LLM. |
| `plots/` | Cartella contenente grafici generati dai dati di consumo energetico. |
| `plots/duration_vs_energy.png` | Grafico rapporto durata/energia. |
| `plots/energy_by_model.png` | Grafico energia per modello. |
| `plots/energy_histogram.png` | Istogramma dei consumi energetici. |
| `plots/energy_time_series.png` | Serie temporale delle misure energetiche. |

### Dettaglio `envTest/`
| Elemento | Descrizione |
|---|---|
| `Lib/` | Pacchetti Python installati nell'ambiente virtuale. |
| `Scripts/` | Script di attivazione dell'ambiente virtuale per Windows. |
| `pyvenv.cfg` | Configurazione dell'ambiente virtuale. |

---

## 🚀 Installazione e Setup

### 1. Ambiente Virtuale
```bash
python -m venv envTest
envTest\Scripts\activate      # Windows
# oppure per Linux/macOS:
# source envTest/bin/activate
```

### 2. Installare Dipendenze
```bash
pip install -r requirements.txt
```

### 3. Configurare `config.json`
Modifica il file con i tuoi parametri:
- IP e credenziali del Raspberry Pi
- Percorsi di `llama.cpp` e del modello
- I prompt da testare

#### Esempio di parametri di `config.json`
| Chiave | Descrizione | Esempio |
|---|---|---|
| `host` | Indirizzo IP del Raspberry Pi | `192.168.0.10` |
| `username` | Nome utente SSH | `pi` |
| `password` | Password SSH | `password` |
| `llama_bin` | Percorso dell'eseguibile `llama-cli` | `./llama.cpp/build/bin/llama-cli` |
| `model_path` | Percorso del file di modello GGUF | `./LLMs/model.gguf` |
| `threads` | Numero di thread per l'inferenza | `4` |
| `prompts` | Array di prompt da inviare al modello | `[...]` |

---

## 🧪 Esecuzione degli Script

### Test SSH (consigliato prima)
```bash
python scripts\SSH_connection_test.py
```

### Test Otii (se hai il dispositivo o almeno l'applicazione desktop Otii 3 con Otii TCP Server attivo)
```bash
python scripts\otii_connection_test.py
```

### Esecuzione Inferenze LLM
```bash
python scripts\LLM_inference_test.py
```

### Genera grafici energetici
```bash
python scripts\plot_energy.py
```

---

## ⚙️ Requisiti di Sistema

- Python 3.x
- Accesso SSH a un Raspberry Pi con `llama.cpp` (versione b8989) installato
- (Opzionale) Dispositivo Otii per il monitoraggio energetico

---

## 📝 Note

- I dati di configurazione sono centralizzati in `config.json` per facilitare le modifiche.
- Lo script `LLM_inference_test.py` estrae metriche di performance (TPS) dall'output di `llama.cpp`.
- Il timeout di default per la lettura dell'output remoto è di 120 secondi (modificabile nel codice).
- `envTest/` contiene l'ambiente virtuale; non è necessario committare nuovamente la cartella se modifichi solo il codice.

---

## Uso

Esegui lo script principale:

```bash
python scripts\LLM_inference_test.py
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
