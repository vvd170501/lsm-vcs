from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum, auto

import click

from ..context import get_context
from ..core.refs import get_head
from ..db import KVDB
from ..db_img import build_image, load_db
from .common import require_repo


@click.command()
# TODO filter by dir
@require_repo
def status():
    for change in sorted(workdir_status(), key=lambda change: change.path):
        print(f'{change.type.name.lower()}: {change.path}')


@dataclass
class Change:
    class Type(Enum):
        ADDED = auto()
        DELETED = auto()
        MODIFIED = auto()

    path: str
    type: Type


def workdir_status() -> Iterator[Change]:
    fs = get_context().fs
    db = load_db(fs)
    if db is None:
        db = KVDB()  # TODO check correctness. Move default to load_db?
    image = build_image(db, get_head()[0])
    for file in fs.rec_iter():
        if file in image:
            content = image[file]
            if content is None:
                if not fs.is_dir(file):
                    yield Change(file, Change.Type.MODIFIED)
            else:
                if fs.is_dir(file) or fs.read_file(file) != content.encode('utf-8'):
                    yield Change(file, Change.Type.CHANGED)
            del image[file]
        else:
            yield Change(file, Change.Type.ADDED)
    for file in image:
        yield Change(file, Change.Type.DELETED)
