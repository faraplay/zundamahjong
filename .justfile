[doc("Show this help message and exit")]
help:
    @just --list


# Hacking on Zundamahjong

[doc("Run the debug Werkzeug server")]
debug-server:
    uv run -m zundamahjong --debug

[doc("Run the debug Vite client")]
debug-client:
    npm --prefix=client run dev


# Running checks on code

[doc("Lint client source code")]
lint-client:
    npm --prefix=client run lint

[doc("Run client tests")]
test-client:
    npm --prefix=client run test

[doc("Run all client checks")]
check-client: lint-client test-client

[doc("Lint server source code")]
lint-server:
    ruff check --select I
    mypy
    basedpyright

[doc("Run server tests")]
test-server:
    pytest

[doc("Run all server checks")]
check-server: lint-server test-server

[doc("Run all checks")]
check-all: check-client check-server
