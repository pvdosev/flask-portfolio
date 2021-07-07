# The Lair of the Gamer Fellowship

![Main page screenshot](https://media.discordapp.net/attachments/851608538710540319/853046071138582538/unknown.png?width=1307&height=630)
A small pixel styled portfolio website with a blog, written with Flask and SQLite!
 

## Installation

### Bare metal:

Make sure you have `python3` and `pip` installed

You will also need a working `postgresql` server on the same machine, or elsewhere.
You can set its location in the .env file.

Create virtual environment using virtualenv
```bash
$ python -m venv python3-virtualenv
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies

```bash
pip install -r requirements.txt
```
### Docker:

Make sure you have `docker` and `docker-compose` installed and running.

Modify the example.env file, and rename it to .env. It will hold the local settings for everything running inside Docker.


## Usage

### Bare metal:
Use development .env file
```
URL=localhost:5000
FLASK_ENV=development
```
Start the Python virtual environment

Linux/MacOS:
```bash
$ source python3-virtualenv/bin/activate
```
Windows:
```
> python3-virtualenv\Scripts\activate.bat
```

Start flask development server
```bash
$ flask run
```

### Docker:

Development:
```bash
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up
```

Production:
```bash
docker-compose -f docker-compose.yml -f docker-compose-prod.yml up
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
