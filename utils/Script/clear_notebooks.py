import nbformat
import os
import copy
from pathlib import Path
def clean_notebook_outputs(path):
    print(f"Checking: {path}")
    with open(path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)

    changed = False

    # Spara original metadata (djup kopia)
    original_metadata = copy.deepcopy(nb.metadata)

    # Rensa outputs från kodceller
    for cell in nb.cells:
        if cell.cell_type == 'code':
            if cell.get("outputs") or cell.get("execution_count") is not None:
                cell["outputs"] = []
                cell["execution_count"] = None
                changed = True

    # Återställ metadata om den har ändrats
    if nb.metadata != original_metadata:
        nb.metadata = original_metadata
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"Cleaned: {path}")
    else:
        print(f" :No changes: {path}")

def find_all_notebooks(root_dir):
    notebooks = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".ipynb"):
                notebooks.append(os.path.join(dirpath, file))
    return notebooks

if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent.parent
    notebooks = find_all_notebooks(repo_root)
    print(f"Found {len(notebooks)} notebooks under {repo_root}")
    for path in notebooks:
        clean_notebook_outputs(path)
