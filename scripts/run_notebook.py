"""Execute a notebook with nbconvert and save an executed copy."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_notebook(notebook_path: str | Path) -> Path:
    """Execute a notebook and save the executed notebook beside it.

    Args:
        notebook_path: Path to the notebook to execute.

    Returns:
        Path to the executed notebook.

    Raises:
        FileNotFoundError: If the notebook is missing.
        subprocess.CalledProcessError: If nbconvert execution fails.
    """
    input_path = Path(notebook_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Notebook not found: {input_path}")

    output_path = input_path.with_name(f"{input_path.stem}.executed.ipynb")
    command = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        str(input_path),
        "--output",
        output_path.name,
        "--output-dir",
        str(output_path.parent),
    ]

    subprocess.run(command, check=True)
    print(output_path)
    return output_path


def main() -> None:
    """Parse CLI arguments and execute the requested notebook."""
    parser = argparse.ArgumentParser(
        description="Run a notebook with jupyter nbconvert."
    )
    parser.add_argument("notebook", help="Path to the notebook to execute.")
    args = parser.parse_args()

    try:
        run_notebook(args.notebook)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        print(
            f"ERROR: Notebook execution failed with code {exc.returncode}",
            file=sys.stderr,
        )
        raise SystemExit(exc.returncode) from exc


if __name__ == "__main__":
    main()
