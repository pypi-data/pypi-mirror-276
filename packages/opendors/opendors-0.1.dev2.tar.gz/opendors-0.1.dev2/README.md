<!--
SPDX-FileCopyrightText: 2023 German Aerospace Center (DLR)
SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>

SPDX-License-Identifier: CC-BY-4.0
-->

# opendors

Library for creating and interacting with the OpenDORS dataset.

## Installation

```shell
# Clone git repository & change into clone directory
git clone git@gitlab.dlr.de:drus_st/opendors.git
cd opendors

# Install with poetry
poetry install
```

## Build Python package

Run `poetry build`.

To publish to PyPI, run `poetry publish`.
You need to have a PyPI API token configured to do this.

## Build conda package

The conda package is configured in `conda/recipe/local/meta.yaml`,
and reuses information from `pyproject.toml`.

To build package locally, run

```shell
# Update to next dev version to keep build metadata intact
poetry version 0.1.dev<n>
conda create -n condabuild conda-build git
conda activate condabuild
conda build conda/recipe/local <optional: --output-folder [FOLDER]>
# e.g.:
#  conda build conda/recipe/local --output-folder /home/stephan/src/opendors/conda-pkgs
```

You can then install the package in a new environment and use it:

```shell
conda create -n my-env --use-local opendors
```

# Run tests

Tests can be run locally as follows:

```bash
poetry run python -m pytest tests/
```

## Test coverage

Coverage (with branch coverage) can be displayed as follows:

```bash
poetry run python -m pytest tests --cov=opendors --cov-branch --cov-report=html --cov-report=term
```
