#!/bin/bash
set -e

APP_DIR="/opt/projector-adb-bridge"
BRANCH="main"

cd "$APP_DIR"

git fetch origin "$BRANCH"
git reset --hard "origin/$BRANCH"

"$APP_DIR/venv/bin/pip" install -r requirements.txt

sudo reboot