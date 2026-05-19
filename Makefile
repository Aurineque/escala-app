.PHONY: lint format test run migrate install docker-build docker-up

help:
	@echo "Comandos disponíveis:"
	@echo "  make lint        — Roda o Ruff como fiscal (lint)"
	@echo "  make format      — Roda o Ruff como arquiteto (formata automático)"
	@echo "  make test        — Roda todos os testes do Django"
	@echo "  make run         — Sobe o servidor local"
	@echo "  make migrate     — Aplica migrações do banco"
	@echo "  make install     — Instala as dependências"
	@echo "  make docker-build — Constrói a imagem Docker"
	@echo "  make docker-up   — Sobe o container"

lint:
	ruff check .

format:
	ruff format .

test:
	python manage.py test --verbosity=2

run:
	python manage.py runserver 8080

migrate:
	python manage.py migrate

install:
	pip install -r requirements.txt

docker-build:
	docker build -t escala-midia .

docker-up:
	docker-compose up --build -d
