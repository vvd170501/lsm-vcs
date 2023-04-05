import click

from .common import require_repo
from ..core.refs import parse_ref, get_head, get_branch_id
from ..context import get_context
from ..db_img import build_image, Image, load_db
from ..strings import splitlines
from ..fs import BaseFS

from os import PathLike
from difflib import context_diff


@click.command()
@click.argument('ref', default='HEAD')
@require_repo
def diff(**kwargs):
    return _diff(**kwargs)


def _get_str_file_contents(fs: BaseFS, file_path: str | PathLike) -> str:
    try:
        file_contents = fs.read_file(file_path).decode('utf-8')
    except UnicodeDecodeError:
        raise click.ClickException(f'Binary files are not supported ({file_path})')
    return file_contents


def _echo_sep(first: bool) -> bool:
    SEP = '\n===============\n'
    if not first:
        click.echo(SEP)
    return False


def _diff(ref: str):
    if ref == 'HEAD':
        ref = get_head()[0]
    else:
        branch_id = get_branch_id(ref)
        if branch_id is None:
            try:
                ref = parse_ref(ref)
            except Exception:
                raise click.ClickException(f'Unknown target: "{ref}" is not a branch name or commit id')
        else:
            ref = branch_id
    fs = get_context().fs
    image: Image = build_image(load_db(fs), ref)
    first = True
    for file_path in fs.rec_iter():
        if file_path in image:
            if fs.is_dir(file_path):
                if image[file_path] is not None:
                    first = _echo_sep(first)
                    click.echo(f'File {file_path} was replaced by an empty directory')
                continue
            file_contents = _get_str_file_contents(fs, file_path)
            if image[file_path] is None:
                first = _echo_sep(first)
                click.echo(f'Empty directory {file_path} was replaced by the following file:')
                for line in splitlines(file_contents):
                    click.echo(f'+ {line}', nl=False)
                continue
            image_contents = image[file_path]
            image_lines = splitlines(image_contents)
            file_lines = splitlines(file_contents)
            to_output = list(context_diff(
                image_lines,
                file_lines,
                fromfile=f'{file_path}: commit',
                tofile=f'{file_path}: file system'
            ))
            if to_output != []:
                first = _echo_sep(first)
                for line in to_output:
                    click.echo(line, nl=False)
                    if line == '' or line[-1] != '\n':
                        click.echo('\n\\ No newline at end of file')
            del image[file_path]
        else:
            if fs.is_dir(file_path):
                was_nonempty = False
                for path in image:
                    if len(path) >= len(file_path) and path[:len(file_path)] == file_path:
                        was_nonempty = True
                if not was_nonempty:
                    first = _echo_sep(first)
                    click.echo(f'New empty directory {file_path}')
                continue
            first = _echo_sep(first)
            click.echo(f'New file {file_path}:')
            file_lines = splitlines(_get_str_file_contents(fs, file_path))
            for line in file_lines:
                click.echo(f'+ {line}', nl=False)
                if line == '' or line[-1] != '\n':
                    click.echo('\n\\ No newline at end of file')
    for file_path in image:
        if image[file_path] is None:
            if not fs.is_dir(file_path):
                first = _echo_sep(first)
                click.echo(f'Empty directory {file_path} was removed')
        else:
            first = _echo_sep(first)
            click.echo(f'File {file_path} was removed:')
            image_lines = splitlines(image[file_path])
            for line in image_lines:
                click.echo(f'- {line}', nl=False)
                if line == '' or line[-1] != '\n':
                    click.echo('\n\\ No newline at end of file')
