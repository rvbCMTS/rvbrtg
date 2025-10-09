import nbformat
import os

def normalize_metadata(path, repo_root):
    with open(path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    changed = False
    langinfo = nb.metadata.get("language_info", {})
    
    if langinfo.get("version") != "3":
        langinfo["version"] = "3"
        changed = True
    if langinfo.get("pygments_lexer") != "ipython3":
        langinfo["pygments_lexer"] = "ipython3"
        changed = True
    nb.metadata["language_info"] = langinfo

    rel_path = os.path.relpath(path, repo_root)

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"Normalized metadata in: {rel_path}")
    else:
        print(f"No metadata changes needed: {rel_path}")

def find_all_notebooks(root_dir):
    notebooks = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(".ipynb"):
                notebooks.append(os.path.join(dirpath, f))
    return notebooks

if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    notebooks = find_all_notebooks(repo_root)
    for path in notebooks:
        normalize_metadata(path, repo_root)
