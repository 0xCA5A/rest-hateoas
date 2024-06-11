# REST HATEOAS Demo

## How to run?
First start:
```shell
make init
make install
make run
```

Check the [Makefile](Makefile) for the available commands.

## How to install more packages?
```shell
venv/bin/pip install foo
venv/bin/pip freeze > requirements.txt
```

## How to build and run a container?
```shell
make container
make container_run
```
