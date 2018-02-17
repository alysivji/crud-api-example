# Repository or specific service
SERVICE =
IMAGE =
help:
	@echo 'Makefile for managing the SivDev Microservice            '
	@echo '                                                         '
	@echo 'Usage:                                                   '
	@echo ' make build      build images                            '
	@echo ' make up         creates containers and starts service   '
	@echo ' make start      starts service containers               '
	@echo ' make stop       stops service containers                '
	@echo ' make down       stops service and removes containers    '
	@echo '                                                         '
	@echo ' make migrate    run migrations                          '
	@echo ' make test       run tests                               '
	@echo ' make test_cov   run tests with coverage.py              '
	@echo '                                                         '
	@echo ' make attach     attach to process inside service        '
	@echo ' make logs       see container logs                      '
	@echo ' make shell      connect to container in new bash shell  '
	@echo '                                                         '

build:
	docker-compose build

up:
	docker-compose up -d api db

start:
	docker-compose start api db

stop:
	docker-compose stop

down:
	docker-compose down

attach: ## Attach to api container
	docker attach api_app

logs:
	docker logs -f api_app

shell: ## Shell into api container
	docker exec -it api_app /bin/bash

migrate: up ## Run migrations using flyway
	docker-compose run --rm migrate

test: migrate
	docker-compose exec api pytest

test_cov: migrate
	docker-compose exec api pytest --verbose --cov

test_view_cov: migrate
	docker-compose exec api pytest --cov --cov-report html && open ./htmlcov/index.html

test_fast: ## Can pass in parameters using p=''
	docker-compose exec api pytest $(p)

# Flake 8
# options: http://flake8.pycqa.org/en/latest/user/options.html
# codes: http://flake8.pycqa.org/en/latest/user/error-codes.html
max_line_length = 100
lint: up
	docker-compose exec api flake8 \
		--max-line-length $(max_line_length)
