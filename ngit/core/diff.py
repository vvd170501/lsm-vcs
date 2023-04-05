import pickle

from sortedcontainers import SortedDict  # type: ignore

from ..db import BaseDB
from .refs import RefId, iterate_history


def get_fs_state(db: BaseDB, commit: RefId) -> tuple[dict[str, list[str]], dict[str, SortedDict[str, str]]]:
    # TODO merge with db_img.image.build_image
    # Build expected file contents
    files: dict[str, SortedDict[str, str]] = dict()
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
    file_contents: dict[str, list[str]] = dict()
    for file_path in files:
        file_contents[file_path] = list(files[file_path].values())
    return file_contents, files
