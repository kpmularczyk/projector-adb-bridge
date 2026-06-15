from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"

LOGS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

def log(message):
    timestamp = datetime.now()

    formatted_message = (
        f"[{timestamp:%Y-%m-%d %H:%M:%S}] {message}"
    )

    print(formatted_message)

    log_filename = f"{timestamp:%Y-%m-%d}.log"
    log_path = LOGS_DIR / log_filename

    with open(log_path, "a", encoding="utf-8") as file:
        file.write(formatted_message + "\n")