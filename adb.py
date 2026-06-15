import subprocess
import os
import platform
import time
from log import log

KEYCODE_POWER = "26"
KEYCODE_ENTER = "66"

if platform.system() == "Windows":
    ADB_PATH = os.path.join(
        os.path.dirname(__file__),
        "platform-tools",
        "adb.exe",
    )
else:
    ADB_PATH = "adb"

def adb_command(args, timeout=15):
    result = subprocess.run(
        [ADB_PATH, *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()

def ensure_adb_server():
    log("starting adb server...")
    result = subprocess.run(
        [ADB_PATH, "start-server"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log(result.stderr)
        raise RuntimeError(result.stderr)

def parse_adb_devices(output: str) -> dict[str, str]:
    lines = output.splitlines()
    devices = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("List of devices"):
            continue
        parts = line.split()
        if len(parts) >= 2:
            serial, state = parts[0], parts[1]
            devices[serial] = state
    return devices

def adb_devices():
    result = subprocess.run(
        [ADB_PATH, "devices"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    log("adb devices")
    devices = parse_adb_devices(result.stdout)
    return devices

def adb_connect(ip: str, port: int = 5555):
    return adb_command(["connect", f"{ip}:{port}"], timeout=10)


def adb_disconnect(ip: str, port: int = 5555):
    return adb_command(["disconnect", f"{ip}:{port}"], timeout=10)




def projector_shutdown(serial: str):
    adb_command(
        ["-s", serial, "shell", "input", "keyevent", KEYCODE_POWER]
    )

    time.sleep(3)

    adb_command(
        ["-s", serial, "shell", "input", "keyevent", KEYCODE_ENTER]
    )