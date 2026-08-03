from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

# Setup project directories
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_build" / "html"
COURSES_DIR = ROOT / "public-modules"


def executable(name: str) -> str:
    """Find a command and provide a useful failure message."""
    candidates = [name, f"{name}.cmd"] if sys.platform == "win32" else [name]
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return path
    raise SystemExit(
        f"Required command '{name}' was not found. "
        "Install the project dependencies described in README.md."
    )

def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)

    marimo = executable("marimo")

    # Define target folder inside the build output
    marimo_output_dir = OUTPUT / "notebooks"
    marimo_output_dir.mkdir(parents=True, exist_ok=True)

    # Find and batch-export all marimo notebooks (.py files) to WASM HTML
    notebooks = [
    f for f in COURSES_DIR.glob("**/*.py") 
    if "tool_library" not in f.name.lower() and "tool_library" not in f.parts
]
    
    if not notebooks:
        print(f"Warning: No notebooks found in {COURSES_DIR}")
    #else:
       # notebook_path = notebooks[0]
       # target_html_path = OUTPUT / "index.html"

    ALLOWED_ASSET_DIRS = ["images", "data", "tool_library"]
    
    for notebook_path in notebooks:
        relative_path = notebook_path.relative_to(COURSES_DIR)
        target_html_path = marimo_output_dir / relative_path.with_suffix(".html")
        target_html_path.parent.mkdir(parents=True, exist_ok=True)

        notebook_folder = notebook_path.parent

        for folder_name in ALLOWED_ASSET_DIRS:
            source_folder = notebook_folder / folder_name

            if source_folder.is_dir():
                # Replicate the folder path structure inside the build folder
                target_folder = target_html_path.parent / folder_name
                shutil.copytree(
                    source_folder, target_folder, dirs_exist_ok=True
                )
                print(f"Bundled asset folder: {folder_name} -> {target_folder}")

        # Build the CLI export command 
        # --mode run: serves the notebook as a clean, interactive app (no code edits allowed)
        # --no-show-code: hides code blocks by default for a polished tutorial look
        run([
            marimo,
            "export",
            "html-wasm",
            str(notebook_path),
            "--output",
            str(target_html_path),
            "--mode", "run",
            "--no-show-code"
        ])

    # Prevent GitHub Pages/Jekyll from ignoring generated asset directories
    (OUTPUT / ".nojekyll").touch()

    print(f"\nBuilt combined site at: {OUTPUT}")


if __name__ == "__main__":
    main()
