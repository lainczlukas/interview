### Installation

Either install [Docker](https://www.docker.com/products/docker-desktop/) or [Python](https://www.python.org/) and [Pipenv](https://pipenv.pypa.io/en/latest/) locally.

### Run with Docker (Recomended)

Run `docker compose up` to start database + web. On first start, web image will be built and then started. To run migrations, just **exec** into web container and run migrations:

```shell
docker compose exec web bash
python manage.py migrate
exit
```

Website will run on localhost:8000

### Run with Pipenv (Not Recomended)

Run `pipenv shell` to enter virtual environment. Then move to directory with `manage.py` file and run `python manage.py runserver 0.0.0.0:8000`.

Be aware that database must be running. Either install PostgreSQL locally (**not recommended**) or start `postgres` container with command:

```shell
docker run --name postgres -e POSTGRES_PASSWORD=<password> -d postgres:13
```

Don't forget to adjust database connection in [settings](violence-prevention/core/settings.py). Instead of using `db` as **host**, you will probably use `localhost` for local DB instances.

Website will run on localhost:8000


### Development
Celkovy cas 7h
setup - 4h
app - 3h