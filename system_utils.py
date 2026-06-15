import subprocess
import platform

from log import log


def is_linux():
    return platform.system() == "Linux"

def restart_network():
    if not is_linux():
        log("restart_network skipped (non-linux platform)")
        return

    log("restarting NetworkManager - started")

    result = subprocess.run(
        ["sudo", "/usr/bin/systemctl", "restart", "NetworkManager"],
        capture_output=True,
        text=True,
        timeout=60,
    )

    log(f"restart NetworkManager returncode: {result.returncode}")
    log(f"restart NetworkManager stdout: {result.stdout.strip()}")
    log(f"restart NetworkManager stderr: {result.stderr.strip()}")

    if result.returncode != 0:
        raise RuntimeError(
            f"NETWORK_RESTART_FAILED: {result.stderr.strip()}"
        )

    log("restarting NetworkManager - finished")


def reboot_system():
    if not is_linux():
        log("reboot_system skipped (non-linux platform)")
        return

    log("rebooting system - started")

    process = subprocess.Popen(
        [
            "sudo",
            "/usr/sbin/reboot",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    log(f"reboot process pid: {process.pid}")

    try:
        stdout, stderr = process.communicate(timeout=10)

        log(f"reboot returncode: {process.returncode}")
        log(f"reboot stdout: {stdout.strip()}")
        log(f"reboot stderr: {stderr.strip()}")

        if process.returncode != 0:
            raise RuntimeError(
                f"REBOOT_FAILED: {stderr.strip()}"
            )

    except subprocess.TimeoutExpired:
        log("reboot command timeout expired (expected if reboot started successfully)")