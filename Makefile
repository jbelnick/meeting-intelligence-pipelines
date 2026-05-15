PYTHON ?= python3
export PYTHONPATH := src

.PHONY: demo scan smoke test verify

demo:
	$(PYTHON) scripts/run_full_demo.py

scan:
	$(PYTHON) scripts/public_safety_scan.py --term "$${BANNED_TERM:-}"

smoke:
	$(PYTHON) scripts/run_full_demo.py

test:
	$(PYTHON) -m unittest discover -s tests -v

verify: test smoke scan
