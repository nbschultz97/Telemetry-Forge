PYTHON ?= python3

install:
	$(PYTHON) -m pip install -e .

run-once:
	ceradon-sam-bot run --config config/config.yaml --once

run-daemon:
	ceradon-sam-bot run --config config/config.yaml --daemon --interval-minutes 1440

backfill:
	ceradon-sam-bot backfill --config config/config.yaml --days 60

test:
	$(PYTHON) -m pytest
