import paramiko

host = "192.168.x.y"
username = "dario"
password = "Tes1&2026"

client = paramiko.SSHClient()

# Accetta automaticamente la chiave host
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connessione
client.connect(hostname=host, username=username, password=password)

# Esegue comando remoto
stdin, stdout, stderr = client.exec_command("pwd")

# Output
print(stdout.read().decode())

# Chiude connessione
client.close()