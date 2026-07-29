# marimo deployment repository

This repository outlines the source configuration for a browser-based Marimo environment for the public modules.

GitHub Actions will build the approved modules on a personal browser and deploy it.

---

## Structure
```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml
├──  scripts/
│   └── build.py
├── .gitignore
├── .nojekyll
└── README.md                       
```

Generated files are written to:

```text
_build/html/
```

The generated `_build/html` directory should not be committed to Git.

---

## Installation
### Prerequisites:
Install the following on your machine:
- Git
- Python 3.10 or newer
- A modern browser such as Chrome, Firefox, Edge, or Safari

### Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

### Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS or Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
python -m pip install marimo
```

---

## Files to Marimo notebooks
### Converting Jupyter notebooks to Marimo notebooks
```bash
marimo convert your_notebook.ipynb -o your_notebook.py
```

## Converting Python scripts to Marimo notebooks
```bash
marimo convert your_script.py -o your_notebook.py
```

### Editing Marimo Files
```bash
marimo edit your_notebook.py --sandbox
```

### Notes for Marimo Run Mode
- **Avoid duplicate and redefining variables**
The same variable cannot be defined in multiple cells. Encapsulate code into functions when possible to minimize global variables and rename duplicate variable names.

- **Include the Inline Script Metadata in the python file**
This will automatically fetch and install dependencies needed for the notebook when exported. The metadata block will automatically generate when running the notebook in Sandbox mode.

- **Replace ``.show()`` functions with ``.gca()``**
Users will be unable to view ``.show()``. ``.gca`` allows users to view the charts in run mode.

- **Including data**
Place them in a folder in the same directory as the notebook. The public folder will be copied to the export directory. To construct the path to your data:
```bash
path_to_csv = mo.notebook_location() / "public" / "data.csv"
df = pl.read_csv(str(path_to_csv))
df.head()
```

- **For more information view the [marimo documentation here](https://docs.marimo.io)**

---

## Build and Run locally
Build the complete notebook:
```python scripts/build.py```
Then open the given link in the terminal.