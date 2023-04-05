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
@click.option('-s', '--short', is_flag=True)
# TODO filter by dir
@require_repo
def status(short: bool):
    for change in sorted(workdir_status(), key=lambda change: change.path):
        if short:
            print(f'{change.type.short} {change.path}')
        else:
            print(f'{change.type.long}: {change.path}')


@dataclass(frozen=True)
class Change:
    class Type(Enum):
        def __new__(cls, value, short: str):
            obj = object.__new__(cls)
            obj._value_ = value
            obj._short = short
            return obj

        ADDED = auto(), '+'
        DELETED = auto(), '-'
        MODIFIED = auto(), 'M'

        @property
        def long(self) -> str:
            return self.name.lower()

        @property
        def short(self) -> str:
            return self._short

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
                    yield Change(file, Change.Type.MODIFIED)
            del image[file]
        else:
            yield Change(file, Change.Type.ADDED)
    for file in image:
        yield Change(file, Change.Type.DELETED)
