# The Lair of the Gamer Fellowship

![Main page screenshot](https://media.discordapp.net/attachments/851608538710540319/853046071138582538/unknown.png?width=1307&height=630)
A small pixel styled portfolio website with a blog, written with Flask and SQLite!
 

## Installation

### Bare metal:

Make sure you have `python3` and `pip` installed

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

Modify the example .env files, which will get loaded by Docker.
They are located inside the `instance` directory.

Run
```bash
docker-compose up
```

## Usage

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

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
