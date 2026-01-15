#!/usr/bin/env bash
set -euo pipefail

CONFIG_PATH="${1:-config/config.yaml}"

ceradon-sam-bot run --config "$CONFIG_PATH" --once
