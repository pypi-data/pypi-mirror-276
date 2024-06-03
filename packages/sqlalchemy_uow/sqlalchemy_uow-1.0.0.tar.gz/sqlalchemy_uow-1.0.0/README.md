# sqlalchemy-uow

Unit of Work for SQLAlchemy project

______________________________________________________________________
[![PyPI Status](https://badge.fury.io/py/sqlalchemy_uow.svg)](https://pypi.org/project/sqlalchemy_uow/)
[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://barbara73.github.io/sqlalchemy_uow/sqlalchemy_uow.html)
[![License](https://img.shields.io/github/license/barbara73/sqlalchemy_uow)](https://github.com/barbara73/sqlalchemy_uow/blob/main/LICENSE)
[![LastCommit](https://img.shields.io/github/last-commit/barbara73/sqlalchemy_uow)](https://github.com/barbara73/sqlalchemy_uow/commits/main)
[![Code Coverage](https://img.shields.io/badge/Coverage-0%25-red.svg)](https://github.com/barbara73/sqlalchemy_uow/tree/main/tests)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/barbara73/sqlalchemy_uow/blob/main/CODE_OF_CONDUCT.md)


Developers:

- Barbara Jesacher (barbarajesacher@icloud.com)


## Setup

### Set up the environment

1. Run `make install`, which installs Poetry (if it isn't already installed), sets up a virtual environment and all Python dependencies therein.
2. Run `source .venv/bin/activate` to activate the virtual environment.

### Install new packages

To install new PyPI packages, run:

```
$ poetry add <package-name>
```

### Auto-generate API documentation

To auto-generate API document for your project, run:

```
$ make docs
```

To view the documentation, run:

```
$ make view-docs
```

## Tools used in this project
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management
* [hydra](https://hydra.cc/): Manage configuration files
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project

## Project structure
```
.
├── .flake8
├── .github
│   └── workflows
│       ├── ci.yaml
│       └── docs.yaml
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── config
│   ├── __init__.py
│   └── config.yaml
├── data
├── makefile
├── models
├── notebooks
├── poetry.toml
├── pyproject.toml
├── src
│   ├── scripts
│   │   ├── fix_dot_env_file.py
│   │   └── versioning.py
│   └── sqlalchemy_uow
│       └── __init__.py
└── tests
    └── __init__.py
```
