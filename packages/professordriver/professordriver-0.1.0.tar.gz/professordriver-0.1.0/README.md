# ProfessorDriver

This package provides a pre-configured Selenium WebDriver with a custom extension and proxy settings.

## Installation

Install from PyPI:

```bash
pip install professordriver
```

## Usage

```python
from professordriver import create_custom_driver

driver = create_custom_driver('185.177.107.30:9871')
```