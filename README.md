# placement
*Production code for Sensor Placement Optimization*

[![Pylint](https://github.com/Hammerling-Research-Group/placement/actions/workflows/pylint.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/pylint.yml)
[![Spell Check](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml)

## Optimal Sensor Placement

We have developed an intelligent and adaptable system designed to optimize the placement of continuous monitoring sensors on oil and gas sites for methane emissions detection. Further, our approach addresses a larger problem scale compared to previous studies and can be customized for various sensor placement objectives.

## Installation & Usage

Though the current code is still in draft (*pre-pypi submission*) form, users are still welcome to engage with it. 

To do so, the simplest approach is to ingest the full repo, and work from the toy example: 

```python
import requests
import zipfile
import os

response = requests.get("https://github.com/Hammerling-Research-Group/placement/archive/refs/heads/main.zip")

with open("placement.zip", 'wb') as f:
    f.write(response.content)

with zipfile.ZipFile("placement.zip", 'r') as zip_ref:
    zip_ref.extractall(os.path.expanduser("~/Desktop/placement")) # or wherever you'd like to store the code
```

## (Evolving) Package Structure

*Note*: structuring according to requirements for submission to pypi, as well as in line with package best practices. 

```bash
placement/
│
├── placement/
│   ├── __init__.py         # Initializes the package
│   ├── step1.py            # First algorithm step
│   ├── step2.py            # Second algorithm step
│   ├── step3.py            # Third algorithm step
│   ├── step4.py            # Fourth algorithm step
│   └── step5.py            # Fifth algorithm step (`PROSS`)
│
├── tests/
│   ├── __init__.py           
│   ├── test_step1.py
│   ├── test_step2.py
│   ├── test_step3.py
│   ├── test_step4.py
│   └── test_step5.py
│
├── docs/                   # Documentation (Note: only for pypi)
│   ├── index.rst           # Main documentation index for Sphinx
│   ├── usage.rst           # Usage examples // instructions (e.g., `test_PROSS`)
│   └── api.rst             # API docs for each module
│
├── LICENSE
├── README.md               # Package description, installation, and usage instructions
├── setup.py                # Setup script for packaging and metadata
├── MANIFEST.in             # Manifest file to include non-code files in the package
├── .gitignore
└── pyproject.toml          # Build configuration file
```
