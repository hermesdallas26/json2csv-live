# Migration Guide: f3ca7aa5 - json_to_csv_api Deprecation

## Overview
This refactor removes the legacy `json_to_csv_api` module in favor of the unified `json2csv` package.

## Breaking Changes
- Module `json_to_csv_api` removed
- Function signatures changed
- Configuration format updated

## Before (Legacy)
```python
from json_to_csv_api import convert, Config

config = Config(delimiter=",", flatten=True)
result = convert(data, config)
```

## After (New)
```python
from json2csv import json_to_csv

result = json_to_csv(
    data,
    delimiter=",",
    flatten=True
)
```

## Migration Steps
1. Update imports:
   ```python
   # Old
   from json_to_csv_api import convert, Config
   
   # New
   from json2csv import json_to_csv
   ```

2. Replace Config objects with direct parameters:
   ```python
   # Old
   config = Config(delimiter=";", max_depth=3)
   convert(data, config)
   
   # New
   json_to_csv(data, delimiter=";", max_flatten_depth=3)
   ```

3. Update error handling:
   ```python
   # Old
   from json_to_csv_api import ConversionError
   
   # New
   # Uses standard ValueError exceptions
   ```

## Timeline
- v0.1.0: Deprecation notice, new API available
- v0.2.0: Legacy API removal (breaking)
