# zundamahjong

(On Linux) To setup the virtual environment and install dependencies, run
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Debug
To run the debug server, open a shell in the base directory of this repo.
Activate the venv with
```sh
source .venv/bin/activate
```
and then start the server by running
```sh
gunicorn --workers 1 --threads 100 --bind 127.0.0.1:5000 src.server:debug_app
```

## Production server
To run the production server, do the same thing as for the debug but change
`src.server:debug_app` to `src.server:app`.
In other words, activate the venv and then run
```sh
gunicorn --workers 1 --threads 100 --bind 127.0.0.1:5000 src.server:app
```

## Credits
Mahjong tile graphics are from [demching.itch.io/mahjong](https://demching.itch.io/mahjong).