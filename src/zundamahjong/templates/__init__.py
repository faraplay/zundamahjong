from importlib.resources import files

from pydantic import BaseModel, TypeAdapter


class ManifestChunk(BaseModel, frozen=True):
    src: str | None = None
    file: str
    css: tuple[str, ...] | None = None
    assets: tuple[str, ...] | None = None
    isEntry: bool | None = None
    name: str | None = None
    imports: tuple[str, ...] | None = None


vite_manifest = TypeAdapter(dict[str, ManifestChunk]).validate_json(
    files("zundamahjong.client").joinpath(".vite/manifest.json").read_bytes()
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
