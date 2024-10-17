# placement
*Production code for Sensor Placement Optimization*

[![Pylint](https://github.com/Hammerling-Research-Group/placement/actions/workflows/pylint.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/pylint.yml)
[![Spell Check](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml)

## Optimal Sensor Placement

We have developed an intelligent and adaptable system designed to optimize the placement of continuous monitoring sensors on oil and gas sites for methane emissions detection. Further, our approach addresses a larger problem scale compared to previous studies and can be customized for various sensor placement objectives.

## Installation

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

## Usage

Once `placement` is local, ensure that input data is properly defined. Examples of this structure along with code that can be adapted to user-specific needs are included in Jupyter Notebooks in `./demo`.

Once input data are developed, run each of the three core scripts in sequence:

  - `simulate_concentrations.py`
  - `evaluate_detection.py`
  - `optimization.py`

Of note, the optimization step calls `PORSS.py`, which contains the core function used in optimization. 

In the current architecture, output data from running this process will be sent to `./demo/output_data/`. Users may easily update these paths if desired. 

## (Evolving) Package Structure

*Note*: structuring according to requirements for submission to pypi, as well as in line with package best practices. 

```bash
placement/
│
├── placement/
│   ├── __init__.py
│   ├── simulate_concentrations.py
│   ├── evaluate_detection.py
│   └── optimization.py
│       └── PORSS.py
│
├── tests/
│   ├── __init__.py           
│   ├── test_simulate_concentrations.py
│   ├── test_evaluate_detection.py
│   └── test_optimization.py
│
├── docs/                   # Documentation (Note: only for pypi)
│   ├── index.rst           # Main documentation index for Sphinx
│   ├── usage.rst           # Usage examples // instructions
│   └── api.rst             # API docs for each module
│
├── LICENSE
├── README.md
├── setup.py                # Setup script for packaging and metadata
├── MANIFEST.in             # Manifest file to include non-code files in the package
├── .gitignore
└── pyproject.toml
```
