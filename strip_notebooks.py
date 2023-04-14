import os
from fnmatch import fnmatch
from nbstripout import strip_output
from nbformat import read, write, NO_CONVERT


def _scan_repo_for_pattern(root_path, pattern):
    """Scan the repo for a specific pattern"""

    hits = []

    for path, subdirs, files in os.walk(root_path):
        for name in files:
            if fnmatch(name, pattern):
                hits.append(os.path.join(path, name))
    
    return hits

# get list of paths to all notebooks in repo
tmp = _scan_repo_for_pattern(root_path='.', pattern= "*.ipynb")
path_to_notebooks = []

# sort out checkpoint files
for item in tmp:
    if 'checkpoint' not in item:
        path_to_notebooks.append(item)

# read notebook
nbs = [read(path, as_version=NO_CONVERT) for path in path_to_notebooks]
# strip output from nb
nb_stripped = [strip_output(nb, keep_output=False, keep_count=False) for nb in nbs]

# write output
[write(nb=nb_stripped[i], fp=path_to_notebooks[i]) for i in range(len(nbs))]
