![Python CI](https://github.com/atchad/ajvpy2/actions/workflows/main.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/ajvpy2.svg)](https://badge.fury.io/py/ajvpy2)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CodeQL](https://github.com/atchad/ajvpy2/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/atchad/ajvpy2/actions/workflows/github-code-scanning/codeql)

# AJVPY2 - Another JSON Schema Validator for Python

This project is a fork of [ajvpy](https://github.com/jdthorpe/ajvpy) with the following changes:
1. Replaced PyV8 with PyMiniRacer.
2. Added support for Python 3.12.

## Installation

1. Install the package from PyPI:
    ```sh
    pip install ajvpy2
    ```

2. (Optional) If you prefer to clone the repository:
    ```sh
    git clone https://github.com/yourusername/ajvpy2.git
    cd ajvpy2
    pip install -r requirements.txt
    ```

## Usage

### Basic Example

```python
from ajv import Ajv

schema = {"type": "integer"}
data = 42

ajv = Ajv()
if ajv.validate(schema, data):
    print("Valid data!")
else:
    print("Invalid data!")
    print(ajv.errors)
```

### Adding Custom Formats

```python
ajv.add_format("customFormat", "^[a-z]+$")
schema = {"type": "string", "format": "customFormat"}
data = "abc"
assert ajv.validate(schema, data)
data_invalid = "ABC123"
assert not ajv.validate(schema, data_invalid)
```

### Adding Custom Keywords

```python
keyword_definition = """
{
    validate: function(schema, data) {
        return schema === data;
    },
    errors: false
}
"""
ajv.add_keyword("testKeyword", keyword_definition)
schema = {"type": "string", "testKeyword": "test"}
data = "test"
assert ajv.validate(schema, data)
data_invalid = "not_test"
assert not ajv.validate(schema, data_invalid)
```

### Using Plugins

```python
plugin_code = """
function myPlugin(ajv) {
    ajv.addKeyword('testKeyword', {
        validate: function(schema, data) {
            return schema === data;
        },
        errors: false
    });
}
"""
ajv.context.eval(plugin_code)
ajv.plugin("myPlugin")
schema = {"type": "string", "testKeyword": "test"}
data = "test"
assert ajv.validate(schema, data)
```

## Running Tests

To run the tests, use `pytest`:

```sh
pytest
```

## License

This project is licensed under the MIT License.
