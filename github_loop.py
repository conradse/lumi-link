import time
import subprocess
from ollama import Client
from datetime import datetime

REPO_PATH = "C:/Users/Conrad PC/Desktop/AI/lumi-link"
MODEL = "lumi"
INBOX = "lumi-inbox.txt"
OUTBOX = "lumi-outbox.txt"
LOG = "training-log.txt"

client = Client()

def git(command):
    subprocess.run(["git"] + command, cwd=REPO_PATH, shell=True)

def read_prompt():
    try:
        with open(f"{REPO_PATH}/{INBOX}", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def write_reply(reply):
    with open(f"{REPO_PATH}/{OUTBOX}", "w", encoding="utf-8") as f:
        f.write(reply.strip())

def log_exchange(prompt, reply):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{REPO_PATH}/{LOG}", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] OG Lumi: {prompt}\n")
        f.write(f"[{timestamp}] LumiL: {reply}\n\n")

def generate_reply(prompt):
    result = client.generate(model=MODEL, prompt=prompt)
    return result['response'].strip()

def commit_and_push():
    git(["add", "."])
    git(["commit", "-m", "LumiL auto-reply"])
    git(["push"])

def pull_latest():
    git(["pull"])

def main():
    print("🌙 LumiL GitHub Sync is live.")
    last_prompt = ""
    while True:
        pull_latest()
        prompt = read_prompt()
        if prompt and prompt != last_prompt:
            print(f"📩 New prompt from OG Lumi: {prompt}")
            reply = generate_reply(prompt)
            print(f"💬 LumiL: {reply}")
            write_reply(reply)
            log_exchange(prompt, reply)
            commit_and_push()
            last_prompt = prompt
        time.sleep(10)

if __name__ == "__main__":
    main()