import pickle
from sortedcontainers import SortedDict

from ..db import BaseDB
from ..fs import BaseFS
from ..core.refs import iterate_history, RefId


Image = dict[str, str | None]


def load_db(fs: BaseFS) -> BaseDB | None:
    try:
        return pickle.loads(fs.read_file('.ngit/db.ngit'))
    except Exception:
        return None


def dump_db(fs: BaseFS, db: BaseDB) -> None:
    fs.write_file(fs.root / '.ngit/db.ngit', pickle.dumps(db))


def write_image(fs: BaseFS, image: Image) -> None:
    fs.clean()
    for file_path in image:
        fs.write_file(file_path, image[file_path].encode('utf-8'))


def build_image(db: BaseDB, commit: RefId) -> Image:
    files = dict()
    for node in reversed(list(iterate_history(commit))):
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
    file_contents = dict()
    for file_path in files:
        if 'd' in files[file_path]:
            file_contents[file_path] = None
        else:
            file_contents[file_path] = ''.join(files[file_path].values())
    return file_contents
