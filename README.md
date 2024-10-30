# placement
*Production code for Sensor Placement Optimization*

[![Spell Check](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml)

## Optimal Sensor Placement

We have developed an intelligent and adaptable system designed to optimize the placement of continuous monitoring sensors on oil and gas sites for methane emissions detection. Further, our approach addresses a larger problem scale compared to previous studies and can be customized for various sensor placement objectives.

Read the [paper associated with this work](https://chemrxiv.org/engage/chemrxiv/article-details/66cd5008a4e53c4876b93af7) for more detail. 

## Installation & Usage

Though the current code is still in draft (*pre-pypi submission*) form, users are still welcome to engage with it. 

To do so, the simplest approach is to ingest the full repo. 

1. Start by creating the environment:

```bash
$ conda env create -f root_environment.yml
```

2. Then, activate it:

```bash
conda activate placement
```

3. Then, run the following to save the full codebase locally (in this example, it would save to your Desktop; update as you'd like):

```python
import requests
import zipfile
import os

response = requests.get("https://github.com/Hammerling-Research-Group/placement/archive/refs/heads/main.zip")

with open("placement.zip", 'wb') as f:
    f.write(response.content)

with zipfile.ZipFile("placement.zip", 'r') as zip_ref:
    zip_ref.extractall(os.path.expanduser("~/Desktop/placement")) # or wherever you'd like
```

4. Once `placement` is local, ensure that input data is properly defined. Examples of this structure along with code that can be adapted to user-specific needs are included as Jupyter Notebooks in `./demo`.

5. Once input data are developed/ingested, run each of the three core scripts in sequence:

  - `simulate_concentrations.py`
  - `evaluate_detection.py`
  - `optimization.py`

In the current architecture, output data from running this process will be sent to `./demo/output_data/`. Users may easily update these paths if desired. 

**Note**: Steps 1 and 2 will eventually be required for integration and working with `pip`. They are not technically required to ingest the repo at the current draft stage of the `placement` codebase. But as they will be eventually needed, we list them here as the place to start. 

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
