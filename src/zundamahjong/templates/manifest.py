from importlib.resources import files

from flask import Flask
from pydantic import BaseModel, TypeAdapter


class ManifestChunk(BaseModel, frozen=True):
    src: str | None = None
    file: str
    css: tuple[str, ...] | None = None
    assets: tuple[str, ...] | None = None
    isEntry: bool | None = None
    name: str | None = None
    imports: tuple[str, ...] | None = None


NO_CLIENT_FILES_ERROR_MESSAGE = """\
*****************************************************
Could not find the needed Zundamahjong client files.
Most likely nothing user-facing will work.
Please run `npm build` inside the `client` directory.
*****************************************************
"""


try:
    vite_manifest = TypeAdapter(dict[str, ManifestChunk]).validate_json(
        files("zundamahjong.client").joinpath(".vite/manifest.json").read_bytes()
    )
except ModuleNotFoundError:
    print(NO_CLIENT_FILES_ERROR_MESSAGE)
    vite_manifest = TypeAdapter(dict[str, ManifestChunk]).validate_python(
        {
            "src/assets/icon.png": {"file": "assets/icon-AAAAAAAA.png"},
            "src/login.tsx": {"file": "assets/login-AAAAAAAA.js", "css": []},
            "src/main.tsx": {"file": "assets/main-AAAAAAAA.js", "css": []},
        }
    )


def imported_chunks(
    manifest: dict[str, ManifestChunk], name: str
) -> set[ManifestChunk]:
    """Recursively follow all chunks from entry point :py:obj:`name`."""

    ret: set[ManifestChunk] = set()

    for import_name in manifest[name].imports or []:
        ret |= imported_chunks(manifest, import_name)
        ret.add(manifest[import_name])

    return ret


def init_app(app: Flask) -> None:
    app.context_processor(lambda: {"manifest": vite_manifest})
    app.add_template_global(imported_chunks)
