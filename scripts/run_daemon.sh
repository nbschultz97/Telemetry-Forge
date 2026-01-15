#!/usr/bin/env bash
set -euo pipefail

CONFIG_PATH="${1:-config/config.yaml}"
INTERVAL_MINUTES="${2:-1440}"

ceradon-sam-bot run --config "$CONFIG_PATH" --daemon --interval-minutes "$INTERVAL_MINUTES"
