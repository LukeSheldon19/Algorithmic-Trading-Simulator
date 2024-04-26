# Django Examples

A starter project for Clark's Databases course (CSCI 220). This project includes a web server and database.

Follow these steps to get started:

## Step 0: Clone This Repository

Unless otherwise specified, all commands mentioned below should be run within the root directory of this repository.

## Step 1: Install Docker

This project includes several components: 

- uWSGI, which will run your Django application code
- NGINX, a web server which will allow browsers to communicate with uWSGI
- PostgresSQL, a database which will store your application's persistent data

It could be time-consuming to install and configure all of these on your computer, but thankfully there is a better way: Docker! [Install Docker](https://docs.docker.com/get-docker/), and it will be easy to run all of these components.

## Step 2: Secure Configuration

It is a terrible idea to run software with default passwords. To configure the password for the database and other settings, you will need to write them in a `.env` file. Follow these steps:

1. Copy `dot_env_example` to `.env`
2. Run `chmod 600 .env` to prevent other users from reading your `.env` file
3. Edit `.env`, changing:
  - The text `RANDOM_PASSWORD` to a password which is actually random
  - The text `SOMETHING_LONG_AND_RANDOM` to random text, ideally generated using the Python one-liner below:

```
python3 -c "import string,random; uni=string.ascii_letters+string.digits; print(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))]))"
```

## Step 3: Start the Docker Services

Run:
```
docker compose up
```

The first time you run it, this command will take a few minutes to complete. This is because Docker needs to download the code for PostgresSQL, etc.

When you are done running the application, you can stop it by typing `Control-C`.

## Step 4: Run Migrations

Follow the instructions below to run the database migrations. This will ensure the database has the schema for the applications.

## Step 5: Load the Applications

Load <http://localhost:8080> and you should be redirected to the "Django administration" login interface.

Load <http://localhost:8080/minifacebook> to view the latest statuses of users of the minifacebook application. See instructions below for using the Django admin interface, which you can use to create users and status updates. 


## Hints

### Creating Admin Accounts

To create a superuser, which can access the Django admin interface:

```
docker compose exec django python manage.py createsuperuser
```

To create a regular user, load `/admin/auth/user/add/` in your browser.

You can then log into the Django admin interface using this superuser account.

### Database Operations

#### Manual Commands

To interactively run SQL commands, run:

```
> docker compose exec postgres bash
# psql --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"
```

#### Migrations

When you edit Django models, the changes don't take effect until you update the database. This is done in two steps.

First, you create a migration file, which describes the changes to be made:

```
docker compose exec django python manage.py makemigrations
```

Then, you apply those changes by running the migration file:

```
docker compose exec django python manage.py migrate
```

You can read more about [Django migrations here](https://docs.djangoproject.com/en/3.2/topics/migrations/).

#### Dump

To dump the SQL commands needed to recreate a database to file, run:

```
> docker compose exec postgres bash
# pg_dump --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --file=/postgres_files/db_dump.DATE.sql
```

#### Load

To execute SQL commands from a file, run:

```
> docker compose exec postgres bash
# psql --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set ON_ERROR_STOP=on --file /postgres_files/db_dump.DATE.sql
```
