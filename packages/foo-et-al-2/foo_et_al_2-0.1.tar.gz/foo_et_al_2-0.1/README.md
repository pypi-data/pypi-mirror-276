# FOO (ET AL)^2
## UCAR Science Feature Toolkit

Foo (Et Al)^2 is a package for calculating the complex Foo et al. parameterization, proposed in 2024 by UCAR researchers Foo, Bar and Baz. In the spirit of open science and scientific progress, we extend an open invitation to contribute new science features alongside the Foo et al. parameterization, making this package Foo et al., et al.; Foo (Et Al)^2

# Contribution Guidelines

## File Strucutre

`foo_et_al_2/foo_et_al` contains files for the core Foo et al. parameterization feature.

`foo_et_al_2/et_al` is the directory for new science feature contributions.

## Code Style
For ease of communication and maintenence, please conform to the PEP 8 Style Guide.

## General Contribution Version Control Guidelines
1. Create and checkout a new working branch from `main` in the GitHub repository
2. Contribute new features or suggest changes to existing features
3. In your terminal, run `python tests/run_tests.py` to test your contribution along with pre-existing tests
4. Commit your changes to the new branch
5. Open a pull request with a description of the change, and request review from a core contributor

### If Contributing New Science Features
1. Create a new package in `foo_et_al_2/et_al` with a descriptive name, say `/_example_contribution`
2. Create your new python files, say `hello_world.py` and `is_palindrome.py` within `/_example_contribution`
3. In `foo_et_al_2/tests` create a test file in the format `test_<new_package_name>.py` with unit tests for all files in your new package

See example contribution files in the file tree.

### If Suggesting Changes to Existing Features

See "Merge Pull Request #1" in GitHub for an example of a successful feature change suggestion.


# Documentation
Read the documentation [here](docs/index.md)

# Installation Instructions


# Citing FOO (ET AL)^2

If you use this software, please cite it as

`FBB Lab. (2024). UCAR Science Feature Toolkit: Foo (Et Al)^2.`