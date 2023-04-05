import click
from difflib import context_diff
import pickle

from ..strings import generate_middle_string
from ..context import get_context
from ..core.diff import get_fs_state
from ..core.refs import Branch, RefId, get_head, set_head, update_branch, ref_to_str
from ..db import KVDB
from ..db_img import load_db, dump_db
from .common import require_repo


@click.command()
@click.option('-m', '--message', required=True)  # interactive editor is not supported
@require_repo
def commit(**kwargs):
    create_commit(**kwargs)


def create_commit(message: str) -> RefId:
    head, current_branch = get_head()
    # XXX save diffs to FS tree in lseqdb, add node ids to commit content (guess this won't be implemented).
    # Use some more complex data type (also need to save merges)

    fs = get_context().fs
    db = load_db(fs)
    if db is None:
        db = KVDB()

    # Not sure if lastdiffs is the correct name
    files_contents, files_lastdiffs = get_fs_state(db, head)

    # Create a new commit
    head = get_context().server.add_node(head, message.encode())
    head_bytes = pickle.dumps(head)

    # Write diffs to db
    for file_path in fs.rec_iter():
        # TODO move to separate function (may be reused for diff/checkout)
        if fs.is_dir(file_path):
            db.insert((head_bytes, file_path + '/d'), '')
        elif file_path in files_lastdiffs:
            lastdiffs = files_lastdiffs[file_path]
            if 'd' in lastdiffs:  # directory
                assert len(lastdiffs) == 1  # TODO check
                lastdiffs.clear()
                files_contents[file_path].clear()
            diff = list(context_diff(files_contents[file_path],
                                     list(map(lambda x: x.decode('utf-8'),
                                              fs.read_file(file_path).splitlines(keepends=True))),
                                     n=0))[2:]
            i = -1
            old = None
            chunk_lengths: list[int] = []
            chunk_i = -1
            was_repl = False
            last_line = None
            for line in diff:
                if line[:4] == '****':
                    chunk_lengths = []
                    continue
                if line[0] == '*':
                    was_repl = False
                    i = int(line.split()[1].split(',')[0]) - 2
                    old = True
                    continue
                if line[:2] == '--':
                    if was_repl:
                        chunk_lengths[-1] = i - chunk_lengths[-1]
                    was_repl = False
                    i = int(line.split()[1].split(',')[0]) - 2
                    chunk_i = 0
                    old = False
                    continue
                if old:
                    i += 1
                    if line[0] != ' ':
                        db.insert((head_bytes, file_path + '/' + lastdiffs.keys()[i] + '-'), '')
                    if line[0] == '!' and not was_repl:
                        chunk_lengths.append(i)
                    if line[0] != '!' and was_repl:
                        chunk_lengths[-1] = i - chunk_lengths[-1]
                else:
                    if line[0] == ' ':
                        if was_repl:
                            i += chunk_lengths[chunk_i]
                            chunk_i += 1
                        else:
                            i += 1
                        last_line = lastdiffs.keys()[i]
                    ni = i + 1
                    if ni == len(lastdiffs):
                        next_line = None
                    else:
                        next_line = lastdiffs.keys()[ni]
                    if line[0] != ' ':
                        new_line = generate_middle_string(last_line, next_line)
                        db.insert((head_bytes, file_path + '/' + new_line), line[2:])
                        last_line = new_line
                was_repl = line[0] == '!'
            del files_lastdiffs[file_path]
        else:
            last_line_key = None
            try:
                lines = fs.read_file(file_path).decode('utf-8').splitlines(keepends=True)
            except UnicodeDecodeError:
                raise click.ClickException(f'Binary files are not supported ({file_path})')
            if lines == []:
                lines = ['']
            for line in lines:
                cur_line_key = generate_middle_string(last_line_key, None)
                db.insert((head_bytes, file_path + '/' + cur_line_key), line)
                last_line_key = cur_line_key
    for deleted_file_path in files_lastdiffs:
        db.insert((head_bytes, str(deleted_file_path) + '/!'), '')

    dump_db(fs, db)

    # Currently, empty commits are allowed. Maybe they will be disabled later
    set_head(head, current_branch)
    if current_branch:
        update_branch(Branch(current_branch, head))
    click.echo(f'Commit {ref_to_str(head)}')
    click.echo(f'Message \'{message}\'')
    return head
