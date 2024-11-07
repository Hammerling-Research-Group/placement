# placement
*Production code for Sensor Placement Optimization*

[![Spell Check](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml)

## Optimal Sensor Placement

We have developed an intelligent and adaptable system designed to optimize the placement of continuous monitoring sensors on oil and gas sites for methane emissions detection. Further, our approach addresses a larger problem scale compared to previous studies and can be customized for various sensor placement objectives.

Read the [paper associated with this work](https://chemrxiv.org/engage/chemrxiv/article-details/66cd5008a4e53c4876b93af7) for more detail. 

## Installation & Usage

Though the current code is still in draft (*pre-pypi submission*) form, users are still welcome to engage with it. 

To do so, the simplest approach is to clone the repo and work from the `placement` directory. 

1. Set your desired directory from which to work. E.g., for your Desktop:

```bash
$ cd Desktop
```

2. Clone and store `placement` at the desired location:

```bash
$ git clone https://github.com/Hammerling-Research-Group/placement.git
```

3. Move into the cloned `placement` directory:

```bash
$ cd placement
```

4. Navigate to root and install:

```bash
pip install -e .
```

*Optional*: 

a. If you haven't already, create the environment unique to `placement`:

```bash
$ conda env create -f root_environment.yml
```

b. Then, activate it:

```bash
conda activate placement
```

When finished and your input data are developed/ingested, run each of the three core scripts in sequence:

  - `simulate_concentrations.py`
  - `evaluate_detection.py`
  - `optimization.py`

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
