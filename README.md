# Falcon CRUD API

This is a project for practicing creating a CRUD API in Falcon and testing it with pytest.

## Makefile Commands

```text
Makefile for managing the SivDev Microservice

Usage:
 make build      build images
 make up         creates containers and starts service
 make start      starts service containers
 make stop       stops service containers
 make down       stops service and removes containers

 make migrate    run migrations
 make test       run tests
 make test_cov   run tests with coverage.py
 make test_fast  run tests without migrations
 make lint       run flake8 lintery

 make attach     attach to process inside service
 make logs       see container logs
 make shell      connect to container in new bash shell
```
