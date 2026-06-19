from __future__ import annotations

import argparse
import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def execute_notebook(path: Path, timeout: int) -> None:
    src_path = str(Path("src").resolve())
    current_pythonpath = os.environ.get("PYTHONPATH", "")
    if src_path not in current_pythonpath.split(os.pathsep):
        os.environ["PYTHONPATH"] = (
            src_path if not current_pythonpath else f"{src_path}{os.pathsep}{current_pythonpath}"
        )

    tmp_path = Path(".tmp").resolve()
    tmp_path.mkdir(exist_ok=True)
    for variable in ("TMPDIR", "TMP", "TEMP"):
        os.environ[variable] = str(tmp_path)

    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(notebook, timeout=timeout, kernel_name="python3")
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta notebooks del proyecto.")
    parser.add_argument("paths", nargs="*", type=Path, help="Notebooks a ejecutar.")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout por celda.")
    args = parser.parse_args()

    paths = args.paths or sorted(Path("notebooks").glob("*.ipynb"))
    if not paths:
        raise SystemExit("No se encontraron notebooks para ejecutar.")

    for path in paths:
        print(f"Ejecutando {path}")
        execute_notebook(path, args.timeout)


if __name__ == "__main__":
    main()
