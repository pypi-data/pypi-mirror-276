# ajvpy2

A thin wrapper around the AJV JSON Validator for Python.

## Installation

```sh
pip install -r requirements.txt
```

## Usage

### Simple Example

```python
from ajvpy2.ajv import Ajv

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
    },
    "required": ["name", "age"],
}

data = {"name": "John Doe", "age": 30}
ajv = Ajv()
validate = ajv.compile(schema)

if validate(data):
    print("Valid data!")
else:
    print("Invalid data!")
    print(ajv.errors)
```

### Complex Example

```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 50},
        "email": {"type": "string", "format": "email"},
        "age": {"type": "integer", "minimum": 18, "maximum": 120},
        "hobbies": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "uniqueItems": True,
        },
    },
    "required": ["name", "email", "age"],
    "additionalProperties": False,
}

data = {
    "name": "Alice Smith",
    "email": "alice@example.com",
    "age": 25,
    "hobbies": ["reading", "swimming", "hiking"],
}

ajv = Ajv()
validate = ajv.compile(schema)

if validate(data):
    print("Valid data!")
else:
    print("Invalid data!")
    print(ajv.errors)
```

## Running Tests

```sh
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
