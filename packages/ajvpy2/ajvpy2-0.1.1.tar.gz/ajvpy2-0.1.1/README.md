# AJV Python Integration

This project integrates the AJV (Another JSON Schema Validator) JavaScript library with Python, allowing for JSON schema validation within Python applications.

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
