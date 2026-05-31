import paramiko
import json

# Carica la configurazione dal file JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

host = config['host']
username = config['username']
password = config['password']

client = paramiko.SSHClient()

# Accetta automaticamente la chiave host
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connessione
client.connect(hostname=host, username=username, password=password)

# Esegue comando remoto
stdin, stdout, stderr = client.exec_command('echo "Ciao sono Raspberry Pi5 e sono connesso correttamente tramite SSH!"')

# Output
print(stdout.read().decode())

# Chiude connessione
client.close()