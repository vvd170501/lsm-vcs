import click
from sortedcontainers import SortedDict
from difflib import context_diff
import pickle

from ..strings import generate_middle_string
from ..context import get_context
from ..core.refs import Branch, get_head, set_head, update_branch
from ..core.nodes import NodeName, resolve_named_node
from .common import require_repo


@click.command()
@click.option('-m', '--message', required=True)  # interactive editor is not supported
@require_repo
def commit(**kwargs):
    _commit(**kwargs)


def _iterate_history(commit):
    commit_tree = resolve_named_node(NodeName.COMMIT_TREE)
    nodes = {node.id: node for node in get_context().server.get_nodes(commit_tree)}
    while commit != commit_tree:
        yield nodes[commit]
        commit = nodes[commit].parent


def _list_subfiles(fs, path: str):
    yield path
    if fs.is_dir(path):
        for filename in fs.iter_dir(path):
            for to_yield in _list_subfiles(filename):
                yield to_yield


def _commit(message: str) -> None:
    head, current_branch = get_head()
    # TODO save diffs to FS tree, add node ids to commit content.
    # Use some more complex data type (also need to save merges)
    context = get_context()
    fs = context.fs
    # textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    # is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    # Currently only support text files
    db = pickle.loads(fs.read_file(fs.root / '.ngit/db.ngit'))
    files = dict()
    for node in reversed(_iterate_history(head)):
        for key in db.filter_by_commit(pickle.dumps(node)):
            path_line = key[1].split('/')
            file_path = '/'.join(path_line[:-1])
            line = path_line[-1]
            if line[-1] == '-':
                del files[file_path][line[:-1]]
            else:
                if file_path not in files:
                    files[file_path] = SortedDict()
                files[file_path][line] = db[key]
    file_contents = dict()
    for file_path in files:
        file_contents[file_path] = ''.join(files[file_path].values())
    # Currently, empty commits are allowed. Maybe they will be disabled later
    head = get_context().server.add_node(head, message.encode())
    head_bytes = pickle.dumps(head)
    for file_path in _list_subfiles(fs.root):
        if file_path in files:
            diff = list(context_diff(files[file_path], fs.read_file(file_path).splitlines(keepends=True), n=0))[2:]
            i = -1
            old = None
            chunk_lengths = []
            chunk_i = -1
            was_repl = False
            # was_plus = False
            last_line = ''
            for line in diff:
                if line[:4] == '****':
                    chunk_lengths = []
                    continue
                if line[0] == '*':
                    was_repl = False
                    i = line.split()[1].split(',')[0] - 2
                    old = True
                    continue
                if line[:2] == '--':
                    if was_repl:
                        chunk_lengths[-1] = i - chunk_lengths[-1]
                    was_repl = False
                    # was_plus = False
                    i = line.split()[1].split(',')[0] - 2
                    chunk_i = 0
                    old = False
                    continue
                if old:
                    i += 1
                    if line[0] != ' ':
                        db.insert((head_bytes, file_path + '/' + files[file_path].keys()[i] + '-'), '')
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
                    ni = i + chunk_lengths[chunk_i] if line[0] == '!' else i + 1
                    next_line = files[file_path].keys()[ni]
                    if line[0] != ' ':
                        new_line = generate_middle_string(last_line, next_line)
                        db.insert((head_bytes, new_line), line[2:])
                        last_line = new_line
                was_repl = line[0] == '!'
                # was_plus = line[0] == '+'
    fs.write_file(fs.root / '.ngit/db.ngit', pickle.dumps(db))
    set_head(head, current_branch)
    if current_branch:
        update_branch(Branch(current_branch, head))
