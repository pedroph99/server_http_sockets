VENV_PYTHON = ./venv/Scripts/python.exe
VENV_PIP = ./venv/Scripts/pip.exe


.PHONY: run, create_venv

run:
	@echo "Iniciando servidor python"
	$(VENV_PIP) install -r requirements.txt
	$(VENV_PYTHON) ./main.py $(SERVER_PORT) $(TYPE_SERVER)


create_venv:
	@echo "Criando ambiente virtual"
	python -m venv venv 
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt