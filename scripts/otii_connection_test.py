from otii_tcp_client import otii_client

try:
    client = otii_client.OtiiClient()

    print("Connessione al server Otii...")

    otii = client.connect()

    print("Server raggiungibile!")

except Exception as e:
    if "Cannot reserve licenses" in str(e):
        print("Server Otii raggiungibile (problema licenza).")
    else:
        print(f"Errore reale di connessione: {e}")