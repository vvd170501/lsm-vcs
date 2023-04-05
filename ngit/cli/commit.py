import click
from sortedcontainers import SortedDict
from difflib import context_diff
import pickle

from ..strings import generate_middle_string
from ..context import get_context
from ..core.refs import Branch, RefId, get_head, iterate_history, set_head, update_branch
from ..db import KVDB
from .common import require_repo
from ..db_img import build_image, load_db, dump_db


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

    # Build expected file contents
    files = dict()
    for node in reversed(list(iterate_history(head))):
        for key in db.filter_by_commit(pickle.dumps(node.id)):  # key = (bin_commit_id, path/line)
            file_path, line = key[1].rsplit('/', 1)
            if line != '' and line[-1] == '-':
                del files[file_path][line[:-1]]
            elif line != '' and line[-1] == '!':
                del files[file_path]
            elif line != '' and line[-1] == 'd':
                files[file_path] = SortedDict({'d': ''})
            else:
                if file_path not in files or 'd' in files[file_path]:
                    files[file_path] = SortedDict()
                files[file_path][line] = db.get(key)
    file_contents = build_image(db, head)
    for file_path in files:
        # if 'd' in files[file_path]:
        #     del files[file_path]['d']
        file_contents[file_path] = list(files[file_path].values())

    # Create a new commit
    head = get_context().server.add_node(head, message.encode())
    head_bytes = pickle.dumps(head)

    # Write diffs to db
    for file_path in fs.list_subfiles(fs.root):
        if fs.is_dir(file_path):
            db.insert((head_bytes, file_path + '/d'), '')
        elif file_path in files:
            if 'd' in files[file_path]:
                del files[file_path]['d']
                file_contents[file_path] = SortedDict()
            # TODO move to separate function (may be reused for diff/show cmds)
            diff = list(context_diff(file_contents[file_path],
                                     list(map(lambda x: x.decode('utf-8'),
                                              fs.read_file(file_path).splitlines(keepends=True))),
                                     n=0))[2:]
            i = -1
            old = None
            chunk_lengths = []
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
                        db.insert((head_bytes, str(file_path) + '/' + files[file_path].keys()[i] + '-'), '')
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
                        last_line = files[file_path].keys()[i]
                    # ni = i + chunk_lengths[chunk_i] if line[0] == '!' else i + 1
                    ni = i + 1
                    if ni == len(files[file_path]):
                        next_line = None
                    else:
                        next_line = files[file_path].keys()[ni]
                    if line[0] != ' ':
                        new_line = generate_middle_string(last_line, next_line)
                        db.insert((head_bytes, str(file_path) + '/' + new_line), line[2:])
                        last_line = new_line
                was_repl = line[0] == '!'
            del files[file_path]
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
                db.insert((head_bytes, str(file_path) + '/' + cur_line_key), line)
                last_line_key = cur_line_key
    for deleted_file_path in files:
        db.insert((head_bytes, str(deleted_file_path) + '/!'), '')

    dump_db(fs, db)

    # Currently, empty commits are allowed. Maybe they will be disabled later
    set_head(head, current_branch)
    if current_branch:
        update_branch(Branch(current_branch, head))
    return head
