# zundamahjong

To setup the Python virtual environment and install dependencies, run

```sh
uv venv
source .venv/bin/activate
uv sync
```

To install the Node.js dependencies, navigate to the `client` folder with

```sh
cd client
```

and then run

```sh
npm install
```

## Debug

To run the debug server, open a shell in the base directory of this repo.
Activate the venv with

```sh
source .venv/bin/activate
```

and then start the Werkzeug server by running

```sh
python -m debug_server
```

To run the debug client, navigate to the folder `client`
and then start the Vite debug server by running

```sh
npm run dev
```

## Production server (Gunicorn server)

To run the production server, open a shell in the base directory of this repo.
Activate the venv with

```sh
source .venv/bin/activate
```

Make sure Gunicorn is installed by running

```sh
uv sync --group=production
```

and then start the Gunicorn server with

```sh
gunicorn --workers 1 --threads 100 --bind 127.0.0.1:5000 zundamahjong.server:app
```

To build the client, open a shell in the `client` folder and run

```sh
npm run build
```

This will output the built client to `client_build`.

Note that Gunicorn does not serve the client files.
You will need to serve the client files separately.

## Generating password hashes

To reset a user's password if they have forgotten it, you can use

```python
>>> from getpass import getpass
>>> from zundamahjong.database.security import hash_pw
>>> print(hash_pw(getpass()))
```

and then input the result manually into the application database.

## Credits

Mahjong tile graphics are from [demching.itch.io/mahjong](https://demching.itch.io/mahjong).
Avatar graphics are by [坂本アヒル](https://www.pixiv.net/en/users/12147115)
