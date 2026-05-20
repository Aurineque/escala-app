PYTHON := $(shell \
	if python3 -c "import django" 2>/dev/null; then echo python3; \
	elif python -c "import django" 2>/dev/null; then echo python; \
	else echo venv/Scripts/python.exe; fi)

.PHONY: lint format test run migrate static install docker-build docker-up

help:
	@echo "Comandos disponiveis:"
	@echo "  make lint        — Roda o Ruff como fiscal (lint)"
	@echo "  make format      — Roda o Ruff como arquiteto (formata automatico)"
	@echo "  make test        — Roda todos os testes do Django"
	@echo "  make run         — Sobe o servidor local"
	@echo "  make static      — Coleta arquivos estaticos (CSS/JS do admin)"
	@echo "  make migrate     — Aplica migracoes do banco"
	@echo "  make install     — Instala as dependencias"
	@echo "  make docker-build — Constroi a imagem Docker"
	@echo "  make docker-up   — Sobe o container"

lint:
	ruff check .

format:
	ruff format .

test:
	$(PYTHON) manage.py test --verbosity=2

run:
	$(PYTHON) manage.py runserver --insecure 8080

static:
	$(PYTHON) manage.py collectstatic --noinput

migrate:
	$(PYTHON) manage.py migrate

install:
	pip install -r requirements.txt

docker-build:
	docker build -t escala-midia .

docker-up:
	docker-compose up --build -d
