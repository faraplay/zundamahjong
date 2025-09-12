# zundamahjong

To install required packages, run (preferably in a venv)
```sh
pip install -r requirements.txt
```

## Debug
To run the debug server, open a shell in the base directory of this repo and run
```sh
gunicorn --workers 1 --threads 100 --bind 127.0.0.1:5000 src.server:debug_app
```

## Credits
Mahjong tile graphics are from [demching.itch.io/mahjong](https://demching.itch.io/mahjong).