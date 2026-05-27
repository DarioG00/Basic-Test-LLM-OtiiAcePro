import paramiko
import re
import random
import time


# =========================
# CONFIG
# =========================

RASPBERRY_IP = "192.168.1.100"
USERNAME = "pi"
PASSWORD = "raspberry"

# path llama.cpp sul raspberry
LLAMA_CPP_DIR = "/home/pi/llama.cpp"

# binario
LLAMA_BIN = "./main"

# modello
MODEL_PATH = "/home/pi/models/mistral-7b-instruct.gguf"

# prompt random
PROMPTS = [
    "Explain quantum mechanics in one sentence.",
    "Write a haiku about Linux.",
    "What is the capital of Japan?",
    "Tell me a joke about programmers.",
    "Summarize the theory of relativity."
]

# numero inferenze
NUM_INFERENCES = 5


# =========================
# REGEX PARSING
# =========================

EVAL_TIME_REGEX = re.compile(
    r"eval time\s*=\s*([\d\.]+)\s*ms.*\(\s*[\d\.]+\s*ms per token,\s*([\d\.]+)\s*tokens per second\)"
)

TOTAL_TIME_REGEX = re.compile(
    r"total time\s*=\s*([\d\.]+)\s*ms"
)


def parse_metrics(output: str):
    """
    Estrae metriche da output llama.cpp
    """

    metrics = {
        "eval_time_ms": None,
        "tokens_per_sec": None,
        "total_time_ms": None
    }

    eval_match = EVAL_TIME_REGEX.search(output)
    if eval_match:
        metrics["eval_time_ms"] = float(eval_match.group(1))
        metrics["tokens_per_sec"] = float(eval_match.group(2))

    total_match = TOTAL_TIME_REGEX.search(output)
    if total_match:
        metrics["total_time_ms"] = float(total_match.group(1))

    return metrics


def build_command(prompt: str):
    """
    Costruisce comando llama.cpp
    """

    cmd = f"""
    cd {LLAMA_CPP_DIR} && \
    {LLAMA_BIN} \
        -m {MODEL_PATH} \
        -p "{prompt}" \
        -n 64 \
        --temp 0.7 \
        --no-display-prompt
    """

    return cmd


def main():

    ssh = paramiko.SSHClient()

    # accetta host key automaticamente
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("Connessione al Raspberry...")

    ssh.connect(
        hostname=RASPBERRY_IP,
        username=USERNAME,
        password=PASSWORD,
        timeout=10
    )

    print("Connesso.\n")

    results = []

    for i in range(NUM_INFERENCES):

        prompt = random.choice(PROMPTS)

        print("=" * 60)
        print(f"Inferenza {i+1}")
        print(f"Prompt: {prompt}")
        print("=" * 60)

        command = build_command(prompt)

        start_time = time.time()

        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode("utf-8", errors="ignore")
        error_output = stderr.read().decode("utf-8", errors="ignore")

        elapsed = time.time() - start_time

        if error_output:
            print("ERROR:")
            print(error_output)

        metrics = parse_metrics(output)

        result = {
            "prompt": prompt,
            "elapsed_s": elapsed,
            **metrics
        }

        results.append(result)

        print("\n--- OUTPUT MODELLO ---\n")
        print(output[-1500:])  # ultimi caratteri

        print("\n--- METRICHE ---")
        print(f"Tempo totale script: {elapsed:.2f} s")
        print(f"Eval time: {metrics['eval_time_ms']} ms")
        print(f"Tokens/sec: {metrics['tokens_per_sec']}")
        print(f"Total time llama.cpp: {metrics['total_time_ms']} ms")
        print()

    ssh.close()

    print("\n========================")
    print("RISULTATI FINALI")
    print("========================")

    for idx, r in enumerate(results):

        print(f"\nInferenza {idx+1}")
        print(f"Prompt: {r['prompt']}")
        print(f"Elapsed: {r['elapsed_s']:.2f} s")
        print(f"Eval time: {r['eval_time_ms']} ms")
        print(f"Tokens/sec: {r['tokens_per_sec']}")
        print(f"Total time: {r['total_time_ms']} ms")


if __name__ == "__main__":
    main()