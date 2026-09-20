import json
import subprocess
import sys
import time
from pathlib import Path

REPO_URL = "https://github.com/Sariel74020/kouyu.git"
ROOT = Path.home() / "kouyu-bridge"
REPO_DIR = ROOT / "repo"
STATE_FILE = ROOT / "processed.json"
WORKBENCH = Path.home() / "english-speaking-workbench"
POLL_SECONDS = 90

def run(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=True, text=True)

def ensure_repo():
    ROOT.mkdir(parents=True, exist_ok=True)
    if not (REPO_DIR / ".git").exists():
        run("git", "clone", REPO_URL, str(REPO_DIR))
    else:
        run("git", "pull", "--ff-only", cwd=REPO_DIR)

def load_processed():
    if not STATE_FILE.exists():
        return set()
    try:
        return set(json.loads(STATE_FILE.read_text(encoding="utf-8")))
    except Exception:
        return set()

def save_processed(ids):
    STATE_FILE.write_text(json.dumps(sorted(ids), ensure_ascii=False, indent=2), encoding="utf-8")

def archive_session(path):
    run(
        sys.executable,
        str(Path.home() / ".codex/skills/kouyu/scripts/workbench.py"),
        "archive", "--input", str(path), "--data-dir", str(WORKBENCH),
    )

def process_inbox(processed):
    inbox = REPO_DIR / "inbox"
    if not inbox.exists():
        return processed
    for path in sorted(inbox.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            session_id = data["id"]
        except Exception as exc:
            print(f"[skip] {path.name}: invalid session JSON: {exc}")
            continue
        if session_id in processed:
            continue
        print(f"[received] {session_id}")
        try:
            archive_session(path)
        except subprocess.CalledProcessError:
            print("[failed] archive failed; will retry next cycle.")
            continue
        processed.add(session_id)
        save_processed(processed)
        print(f"[archived] {session_id}")
    return processed

def main():
    print("Kouyu Bridge started. Checking GitHub -> local workbench every 90 seconds.")
    processed = load_processed()
    while True:
        try:
            ensure_repo()
            processed = process_inbox(processed)
        except Exception as exc:
            print(f"[temporary error] {exc}")
        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
