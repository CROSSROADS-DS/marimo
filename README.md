# marimo deployment repository

This repository outlines the source configuration for a browser-based Marimo environment for the public modules.

GitHub Actions will build the approved modules on a personal browser and deploy it.

## Structure
```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml
│   └── scripts/
│       └── build.py
├── .gitignore
├── .nojekyll
└── README.md                       
```

Generated files are written to:
```_build\html\notebooks```