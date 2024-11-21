# placement
*Production code for Sensor Placement Optimization*

[![Spell Check](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml)
[![Pylint](https://github.com/Hammerling-Research-Group/placement/actions/workflows/pylint.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/pylint.yml)

## Optimal Sensor Placement

We have developed an intelligent and adaptable system designed to optimize the placement of continuous monitoring sensors on oil and gas sites for methane emissions detection. Further, our approach addresses a larger problem scale compared to previous studies and can be customized for various sensor placement objectives.

Read the [paper associated with this work](https://chemrxiv.org/engage/chemrxiv/article-details/66cd5008a4e53c4876b93af7) for more detail. 

## Installation & Usage

To run and engage with the code, the simplest approach is to follow these steps to clone and work from the `placement` directory within the `gp` environment:

```bash
cd Desktop # optional
```

```bash
git clone https://github.com/Hammerling-Research-Group/placement.git
```

```bash
cd placement
```

```bash
conda env update -f root_environment.yml # optional *if* run before
```

```bash
git clone https://github.com/rykerfish/FastGaussianPuff.git
```

```bash
cd FastGaussianPuff
```

```bash
conda env update -f environment.yml # optional *if* run before
```

```bash
conda activate gp
```

```bash
pip install .
```

```bash
cd ..
```

*Of note:* Though there are several steps required, `placement` relies heavily on the [`FastGaussianPuff`](https://github.com/rykerfish/FastGaussianPuff) module, which is in active dev. Hence the need to ensure the latest version of both `placement` and `FastGaussianPuff` are installed each session. 

When finished and input data are either developed or ingested (see the following section for a clearer understanding of the directory structure), users may run each of the three core scripts in sequence (as well as the unit testing suite, each prefixed by `test_*`):

  - `simulate_concentrations.py`
  - `evaluate_detection.py`
  - `optimization.py`

In the current architecture, output data from running this process will be sent to `./demo/output_data/`. Users may easily update these paths if desired. 

## Testing

Users are encouraged to test the `placement` codebase as well. Our testing framework leverages `pytest`, so be sure to call `pytest` instead of `python` when testing. See the following examples for more. 

To test all main step scripts (3 in total), run: 

```bash
pytest tests/
```

To test individual scripts, run, e.g.:

```bash
pytest tests/test_optimization.py
```

## (Evolving) Package Structure

*Note*: structuring according to requirements for submission to pypi, as well as in line with package best practices. 

```
placement/
│
├── placement/
│   ├── __init__.py
│   ├── simulate_concentrations.py
│   ├── evaluate_detection.py
│   └── optimization.py
│   └── PORSS.py
│
├── tests/
│   ├── __init__.py           
│   ├── test_simulate_concentrations.py
│   ├── test_evaluate_detection.py
│   └── test_optimization.py
│
├── docs/                   # Documentation (Note: only for pypi)
│   ├── index.rst           # Main documentation index for Sphinx
│   └── api.rst             # API docs for each module
│
├── demo
│   ├── input_data
│   ├── output_data
│   ├── results_fenceline_locations
│   ├── step1_generate_emission_scenarios.ipynb
│   ├── step2_specify_sensor_locations.ipynb
├── LICENSE
├── README.md
├── setup.py                # Setup script for packaging and metadata
├── MANIFEST.in             # Manifest file to include non-code files in the package
├── .gitignore
└── pyproject.toml
```
