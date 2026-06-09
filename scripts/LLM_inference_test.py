import paramiko
import re
import time
import json

# =========================
# CONFIG
# =========================

with open("config.json", "r") as f:
    config = json.load(f)

RASPBERRY_IP = config["host"]
USERNAME = config["username"]
PASSWORD = config["password"]

LLAMA_BIN = config["llama_bin"]
MODEL_PATH = config["model_paths"]
PROMPTS = config["prompts"]
THREADS = config["threads"]


# =========================
# BUILD COMMAND
# =========================

def build_command():

    cmd = f"""
    {LLAMA_BIN} \
        -m {MODEL_PATH[0]} \
        -c 512 \
        -n 128 \
        -t {THREADS[2]}
    """

    return cmd


# =========================
# PARSE TPS
# =========================

def parse_performance_indicators(output: str):

    metrics = {
        "prompt_tps": None,
        "generation_tps": None
    }

    pattern = (
        r"Prompt:\s*([\d.,]+)\s*t/s\s*\|\s*"
        r"Generation:\s*([\d.,]+)\s*t/s"
    )

    match = re.search(pattern, output)

    if match:
        metrics["prompt_tps"] = float(
            match.group(1).replace(",", ".")
        )

        metrics["generation_tps"] = float(
            match.group(2).replace(",", ".")
        )

    return metrics


# =========================
# READ UNTIL PROMPT
# =========================

def read_until_prompt(channel, timeout=120):

    output = ""
    start = time.time()

    while True:

        if channel.recv_ready():

            chunk = channel.recv(4096)

            if not chunk:
                break

            text = chunk.decode("utf-8", errors="ignore")
            output += text

            # DEBUG LIVE OUTPUT
            print(text, end="", flush=True)

            # llama.cpp pronto per nuovo input
            if output.rstrip().endswith(">"):
                break

        else:

            if time.time() - start > timeout:
                print("\n[TIMEOUT LETTURA]")
                break

            time.sleep(0.05)

    return output


# =========================
# MAIN
# =========================

def main():

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("Connessione SSH...")

    ssh.connect(
        hostname=RASPBERRY_IP,
        username=USERNAME,
        password=PASSWORD
    )

    print("Connesso.\n")

    # =========================
    # START MODEL
    # =========================

    command = build_command()

    print("Avvio modello...\n")

    stdin, stdout, stderr = ssh.exec_command(
        command,
        get_pty=True
    )

    channel = stdout.channel

    # attende startup
    startup_output = read_until_prompt(channel, timeout=60)

    print("\n===== MODEL READY =====\n")

    results = []

    # =========================
    # INFERENCE LOOP
    # =========================

    for idx, prompt in enumerate(PROMPTS):

        print("\n" + "=" * 60)
        print(f"Inferenza {idx + 1}")
        print("=" * 60)

        start_time = time.time()

        # invia prompt
        stdin.write(prompt + "\n")
        stdin.flush()

        # legge risposta fino al nuovo prompt ">"
        output = read_until_prompt(channel)

        elapsed = time.time() - start_time

        metrics = parse_performance_indicators(output)

        result = {
            "prompt": prompt,
            "elapsed_s": elapsed,
            "prompt_tps": metrics["prompt_tps"],
            "generation_tps": metrics["generation_tps"]
        }

        results.append(result)

        print("\n--- METRICHE ---")
        print(f"Elapsed: {elapsed:.2f} s")
        print(f"Prompt TPS: {metrics['prompt_tps']}")
        print(f"Generation TPS: {metrics['generation_tps']}")

    # =========================
    # TERMINAZIONE
    # =========================

    print("\nChiudo modello...")

    try:
        stdin.write("\x03")  # CTRL+C
        stdin.flush()
    except:
        pass

    time.sleep(1)

    ssh.close()

    # =========================
    # SUMMARY
    # =========================

    print("\n========================")
    print("RISULTATI FINALI")
    print("========================")

    for idx, r in enumerate(results):

        print(f"\nInferenza {idx + 1}")
        print(f"Prompt: {r['prompt']}")
        print(f"Elapsed: {r['elapsed_s']:.2f} s")
        print(f"Prompt TPS: {r['prompt_tps']}")
        print(f"Generation TPS: {r['generation_tps']}")


if __name__ == "__main__":
    main()