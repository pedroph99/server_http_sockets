VENV_PYTHON = ./venv/bin/python
VENV_PIP = ./venv/bin/pip

.PHONY: run

run:
	@echo "Iniciando servidor python"
	$(VENV_PIP) install -r requirements.txt
	$(VENV_PYTHON) ./main.py