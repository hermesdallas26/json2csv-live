# JSON to CSV Converter

A robust Python CLI tool for converting JSON data to CSV format with advanced features like nested JSON flattening, custom delimiters, and flexible input/output handling.

## Features

- **Read JSON from file or stdin**: Accept input from files or pipe data directly
- **Output to file or stdout**: Save to file or output to standard output
- **Nested JSON Flattening**: Automatically flatten nested structures using dot notation
- **Custom Delimiters**: Support for custom CSV delimiters
- **Depth Control**: Configure maximum flattening depth
- **Robust Error Handling**: Clear error messages for invalid inputs
- **Type Safety**: Full type hints throughout

## Installation

### From Source

```bash
git clone https://github.com/devorg/json2csv-converter.git
cd json2csv-converter
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```bash
# Convert JSON file to CSV
json2csv input.json -o output.csv

# Convert using stdin
cat data.json | json2csv > output.csv

# Convert using pipe
echo '{"name": "John", "age": 30}' | json2csv
```

### Advanced Options

```bash
# Custom delimiter (semicolon)
json2csv data.json -o output.csv -d ";"

# No flattening (keep nested structure as JSON)
json2csv nested.json --no-flatten

# Limit flattening depth
json2csv deep.json --max-depth 2

# Verbose output
json2csv data.json -v
```

### Nested JSON Handling

Input JSON with nested objects:
```json
{
  "user": {
    "name": "Alice",
    "address": {
      "city": "NYC",
      "zip": "10001"
    }
  },
  "id": 123
}
```

Output with flattening (default):
```csv
id,user.name,user.address.city,user.address.zip
123,Alice,NYC,10001
```

Output with --no-flatten:
```csv
id,user
123,"{""name"":""Alice"",""address"":{}}"
```

## CLI Reference

```
usage: json2csv [-h] [-o FILE] [-d CHAR] [--no-flatten] [--max-depth N]
                [--keep-nested] [-p] [-v] [--version]
                [input]

Convert JSON data to CSV format with nested flattening support.

positional arguments:
  input                 Input JSON file (default: stdin)

optional arguments:
  -h, --help            Show help message and exit
  -o FILE, --output FILE
                        Output CSV file (default: stdout)
  -d CHAR, --delimiter CHAR
                        CSV delimiter character (default: comma)
  --no-flatten          Disable automatic flattening of nested JSON objects
  --max-depth N         Maximum depth for flattening nested objects
  --keep-nested         Keep nested objects as JSON strings when not flattening
  -p, --pretty          Format output with aligned columns
  -v, --verbose         Enable verbose output
  --version             Show program version and exit

Examples:
  json2csv input.json -o output.csv
  cat data.json | json2csv > output.csv
  json2csv --input data.json --delimiter ';'
  echo '{"a":{"b":1}}' | json2csv --no-flatten
```

## Python API

The tool can also be used programmatically:

```python
from json2csv import json_to_csv, flatten_dict
import json

# Using json_to_csv function
data = [
    {"name": "Alice", "details": {"age": 30, "city": "NYC"}},
    {"name": "Bob", "details": {"age": 25, "city": "LA"}}
]

# Convert to CSV string
csv_output = json_to_csv(data)
print(csv_output)

# Output:
# details.age,details.city,name
# 30,NYC,Alice
# 25,LA,Bob

# Custom delimiter
csv_output = json_to_csv(data, delimiter=";")

# Just flatten a dictionary
flat = flatten_dict({"a": {"b": {"c": 1}}})
# Result: {'a.b.c': 1}
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/json2csv
isort src/json2csv
```

### Type Checking

```bash
mypy src/json2csv
```

## Examples

### Array of Objects

```bash
echo '[
  {"name": "Product A", "price": 29.99, "category": "Electronics"},
  {"name": "Product B", "price": 49.99, "category": "Electronics"}
]' | json2csv
```

Output:
```csv
category,name,price
Electronics,Product A,29.99
Electronics,Product B,49.99
```

### Deeply Nested JSON

```bash
echo '{
  "company": "TechCorp",
  "employees": [
    {"name": "John", "department": {"name": "Engineering", "floor": 3}}
  ]
}' | json2csv
```

### Custom Delimiter

```bash
json2csv data.json -d ";" -o output.csv
```

Output uses semicolon separator:
```csv
name;age;city
Alice;30;NYC
Bob;25;LA
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please submit pull requests with tests coverage.
