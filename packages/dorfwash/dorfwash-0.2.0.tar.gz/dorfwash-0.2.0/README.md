# dorfwash

`dorfwash` lets you monitor your Miele washing machines
via the Miele Professional IP Profile API.

`dorfwash` uses [washpy](https://pypi.org/project/washpy/) 
to communicate with the Miele washing machines.

## Usage

There are multiple options on how to run `dorfwash`.

### poetry

run
```bash
poetry run python dorfwash config.json
```
See [config.json](config.json) for an example configuration.

### docker

`dorfwash` provides a small [Dockerfile](Dockerfile), 
so you can build your own `dorfwash` docker container.

```bash
docker build -t dorfwash .
```

You need to mount a valid `config.json` file at
`/config/config.json` in the container to run it.

Also, in [docker-compose](docker-compose) is an example `docker-compose.yml`.
This way, you can just run
```bash
docker compose up
```
to build, mount the config, and run the server.


## Miele IP Profie API

For further information see [washpy](https://pypi.org/project/washpy/)
