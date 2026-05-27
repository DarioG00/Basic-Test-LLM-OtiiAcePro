# BasicTestLLM — Test connessione Otii Server

Repository minimo per verificare la connessione a un Otii Server usando il client Python `otii-tcp-client`.

File principali
- [otii_connection_test.py](otii_connection_test.py): script minimale che apre una connessione TCP al server Otii e stampa la risposta.

Requisiti
- Python 3.8+
- Il package `otii-tcp-client` (nome pacchetto PyPI: `otii-tcp-client`).

Installazione
```bash
python -m pip install -r requirements.txt
# oppure solo il client:
python -m pip install otii-tcp-client
```

Uso
```bash
python otii_connection_test.py
```

Comportamento
- Il file prova a connettersi a `127.0.0.1:1905` con timeout breve.
- In caso di successo stampa la risposta del server e termina con exit code `0`.
- In caso di errore stampa l'eccezione e termina con exit code `1`.

Note
- Se usi un virtualenv, attivalo prima di installare o eseguire lo script.
- Per modificare host/porta editare direttamente `otii_connection_test.py`.
