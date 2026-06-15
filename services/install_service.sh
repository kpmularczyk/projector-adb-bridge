#!/bin/bash
set -e

APP_DIR="/opt/projector-adb-bridge"
SERVICE_NAME="projector-adb-bridge"
SERVICE_FILE="$APP_DIR/systemd/$SERVICE_NAME.service"

echo "Installing systemd service..."

sudo cp "$SERVICE_FILE" "/etc/systemd/system/$SERVICE_NAME.service"

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "Service installed and started."
echo "Status:"
sudo systemctl status "$SERVICE_NAME" --no-pager