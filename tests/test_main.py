"""Tests for json2csv main module."""

import json
import os
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from json2csv.main import flatten_dict, json_to_csv, main


class TestFlattenDict:
    """Test the flatten_dict function."""

    def test_simple_dict(self):
        """Test flattening a simple flat dictionary."""
        data = {"name": "test", "value": 123}
        assert flatten_dict(data) == {"name": "test", "value": 123}

    def test_nested_dict(self):
        """Test flattening a nested dictionary."""
        data = {"user": {"name": "test", "age": 30}}
        assert flatten_dict(data) == {"user.name": "test", "user.age": 30}

    def test_deeply_nested(self):
        """Test three levels of nesting."""
        data = {"a": {"b": {"c": 1}}}
        assert flatten_dict(data) == {"a.b.c": 1}

    def test_max_depth(self):
        """Test max_depth parameter - stop flattening at specified depth."""
        data = {"a": {"b": {"c": 1}}}
        # max_depth=1 means only flatten 1 level deep
        result = flatten_dict(data, max_depth=1)
        # At depth 1, "a" is flattened to "a.b" but its value stays as dict
        assert result == {"a.b": {"c": 1}}


class TestJsonToCsv:
    """Test the json_to_csv function."""

    def test_basic_conversion(self, tmp_path):
        """Test basic JSON to CSV conversion."""
        input_file = tmp_path / "input.json"
        input_data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        input_file.write_text(json.dumps(input_data))

        # Read and parse JSON, then convert
        parsed_data = json.loads(input_file.read_text())
        output_file = tmp_path / "output.csv"
        
        with open(output_file, "w", newline="") as f:
            json_to_csv(parsed_data, output=f)

        content = output_file.read_text()
        # CSV columns are sorted alphabetically: age,name
        # Data follows column order: 30,Alice and 25,Bob
        assert "age,name" in content
        assert "30,Alice" in content
        assert "25,Bob" in content


class TestMainCLI:
    """Test the CLI main function."""

    def test_cli_help(self):
        """Test CLI help output."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])
        assert exc_info.value.code == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
