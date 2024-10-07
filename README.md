# placement
*Production code for Sensor Placement Optimization*

[![Pylint](https://github.com/Hammerling-Research-Group/placement/actions/workflows/pylint.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/pylint.yml)
[![Spell Check](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml/badge.svg)](https://github.com/Hammerling-Research-Group/placement/actions/workflows/spellcheck.yml)

## Optimal CMS Placement

(Eventual) Package Structure: 

*Note*: structuring according to requirements for submission to pypi, as well as in line with package best practices. 

```bash
placement/
│
├── placement/              # Main package directory
│   ├── __init__.py         # Initializes the package
│   ├── step1.py            # First algorithm step
│   ├── step2.py            # Second algorithm step
│   ├── step3.py            # Third algorithm step
│   ├── step4.py            # Fourth algorithm step
│   └── step5.py            # Fifth algorithm step (`PROSS`)
│
├── tests/                  # Test suite
│   ├── __init__.py           
│   ├── test_step1.py       # Tests for step1
│   ├── test_step2.py       # Tests for step2
│   ├── test_step3.py       # Tests for step3
│   ├── test_step4.py       # Tests for step4
│   └── test_step5.py       # Tests for step5
│
├── docs/                   # Documentation (optional for pypi)
│   ├── index.rst           # Main documentation index for Sphinx
│   ├── usage.rst           # Usage examples // instructions (e.g., `test_PROSS`)
│   └── api.rst             # API docs for each module
│
├── LICENSE                 # License file (e.g., MIT License)
├── README.md               # Package description, installation, and usage instructions
├── setup.py                # Setup script for packaging and metadata
├── MANIFEST.in             # Manifest file to include non-code files in the package
├── .gitignore              # Git ignore file to exclude unnecessary files from version control per usual
└── pyproject.toml          # Build configuration file (if needed)
```
