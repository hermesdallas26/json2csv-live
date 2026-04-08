"""Main module for JSON to CSV converter CLI tool."""

import argparse
import csv
import json
import logging
import sys
from collections.abc import MutableMapping
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO, Union

# Configure logging
logger = logging.getLogger(__name__)


def flatten_dict(
    d: Dict[str, Any],
    parent_key: str = "",
    separator: str = ".",
    max_depth: Optional[int] = None,
    current_depth: int = 0,
) -> Dict[str, Any]:
    """
    Flatten a nested dictionary using dot notation.
    
    Args:
        d: The dictionary to flatten
        parent_key: The parent key for recursion
        separator: The separator to use for nested keys
        max_depth: Maximum depth to flatten (None for unlimited)
        current_depth: Current recursion depth
        
    Returns:
        Flattened dictionary with dot-notation keys
    """
    items: List[tuple] = []
    
    for k, v in d.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k
        
        if max_depth is not None and current_depth >= max_depth:
            items.append((new_key, v))
        elif isinstance(v, MutableMapping) and v:
            items.extend(
                flatten_dict(
                    v, new_key, separator, max_depth, current_depth + 1
                ).items()
            )
        else:
            items.append((new_key, v))
    
    return dict(items)


def normalize_value(value: Any) -> str:
    """
    Convert a value to a string suitable for CSV output.
    
    Args:
        value: Any value to convert
        
    Returns:
        String representation of the value
    """
    if value is None:
        return ""
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (list, tuple)):
        return json.dumps(value)
    elif isinstance(value, dict):
        return json.dumps(value)
    else:
        return str(value)


def get_all_keys(data: List[Dict[str, Any]]) -> List[str]:
    """
    Get all unique keys from a list of dictionaries.
    
    Args:
        data: List of dictionaries
        
    Returns:
        Sorted list of unique keys
    """
    keys = set()
    for item in data:
        keys.update(item.keys())
    return sorted(keys)


def json_to_csv(
    json_data: Union[List[Dict], Dict],
    output: Optional[TextIO] = None,
    delimiter: str = ",",
    flatten: bool = True,
    max_flatten_depth: Optional[int] = None,
    keep_nested: bool = False,
) -> Optional[str]:
    """
    Convert JSON data to CSV format.
    
    Args:
        json_data: JSON data as dict or list of dicts
        output: Output file handle (None to return as string)
        delimiter: CSV delimiter character
        flatten: Whether to flatten nested JSON structures
        max_flatten_depth: Maximum depth for flattening
        keep_nested: Keep nested JSON as JSON strings when not flattening
        
    Returns:
        CSV string if output is None, otherwise None
    """
    # Normalize input to list of dicts
    if isinstance(json_data, dict):
        records = [json_data]
    elif isinstance(json_data, list):
        records = json_data
    else:
        raise ValueError(f"Expected dict or list of dicts, got {type(json_data).__name__}")
    
    if not records:
        raise ValueError("No records to convert")
    
    # Process records
    processed_records = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError(f"Expected dict record, got {type(record).__name__}")
        
        if flatten:
            # Flatten nested dictionaries
            processed = flatten_dict(record, max_depth=max_flatten_depth)
        elif keep_nested:
            # Convert nested objects to JSON strings
            processed = {
                k: (json.dumps(v) if isinstance(v, (dict, list)) else v)
                for k, v in record.items()
            }
        else:
            processed = record
        
        # Normalize all values to strings
        processed = {k: normalize_value(v) for k, v in processed.items()}
        processed_records.append(processed)
    
    # Get all fieldnames from all records
    fieldnames = get_all_keys(processed_records)
    
    # Create output buffer
    if output is None:
        output_buffer = StringIO()
    else:
        output_buffer = output
    
    # Write CSV
    writer = csv.DictWriter(
        output_buffer,
        fieldnames=fieldnames,
        delimiter=delimiter,
        extrasaction="ignore",
        quoting=csv.QUOTE_MINIMAL,
    )
    writer.writeheader()
    writer.writerows(processed_records)
    
    if isinstance(output_buffer, StringIO):
        return output_buffer.getvalue()
    return None


def read_json_input(input_source: Optional[TextIO] = None) -> Any:
    """
    Read JSON data from file or stdin.
    
    Args:
        input_source: File handle to read from (None for stdin)
        
    Returns:
        Parsed JSON data
    """
    try:
        if input_source is None:
            content = sys.stdin.read()
        else:
            content = input_source.read()
        
        if not content.strip():
            raise ValueError("Empty input")
        
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="json2csv",
        description="Convert JSON data to CSV format with nested flattening support.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  json2csv input.json -o output.csv
  cat data.json | json2csv > output.csv
  json2csv --input data.json --delimiter ';'
  echo '{"a":{"b":1}}' | json2csv --no-flatten

For more information, visit the project documentation.
        """,
    )
    
    parser.add_argument(
        "input",
        nargs="?",
        type=argparse.FileType("r"),
        help="Input JSON file (default: stdin)",
    )
    
    parser.add_argument(
        "-o", "--output",
        type=argparse.FileType("w"),
        metavar="FILE",
        help="Output CSV file (default: stdout)",
    )
    
    parser.add_argument(
        "-d", "--delimiter",
        default=",",
        metavar="CHAR",
        help="CSV delimiter character (default: comma)",
    )
    
    parser.add_argument(
        "--no-flatten",
        action="store_true",
        help="Disable automatic flattening of nested JSON objects",
    )
    
    parser.add_argument(
        "--max-depth",
        type=int,
        metavar="N",
        help="Maximum depth for flattening nested objects",
    )
    
    parser.add_argument(
        "--keep-nested",
        action="store_true",
        help="Keep nested objects as JSON strings when not flattening",
    )
    
    parser.add_argument(
        "-p", "--pretty",
        action="store_true",
        help="Format output with aligned columns (uses pandas if available)",
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args: Command line arguments (default: sys.argv[1:])
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_argument_parser()
    parsed_args = parser.parse_args(args)
    
    # Configure logging based on verbose flag
    log_level = logging.INFO if parsed_args.verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s',
        stream=sys.stderr
    )
    
    try:
        # Read input
        if parsed_args.verbose:
            logger.info("Reading JSON input...")
        
        json_data = read_json_input(parsed_args.input)
        
        if parsed_args.verbose:
            count = len(json_data) if isinstance(json_data, list) else 1
            logger.info(f"Read {count} record(s)")
        
        # Convert to CSV
        if parsed_args.verbose:
            logger.info("Converting to CSV...")
        
        csv_output = json_to_csv(
            json_data,
            output=parsed_args.output,
            delimiter=parsed_args.delimiter,
            flatten=not parsed_args.no_flatten,
            max_flatten_depth=parsed_args.max_depth,
            keep_nested=parsed_args.keep_nested,
        )
        
        # Output result
        if csv_output is not None:
            print(csv_output)
        
        if parsed_args.verbose:
            logger.info("Conversion complete!")
        
        return 0
        
    except ValueError as e:
        logger.error(f"Error: {e}")
        return 1
    except FileNotFoundError as e:
        logger.error(f"Error: File not found - {e}")
        return 1
    except PermissionError as e:
        logger.error(f"Error: Permission denied - {e}")
        return 1
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Error: Unexpected error - {e}")
        return 1
    finally:
        # Close file handles
        if parsed_args.input:
            parsed_args.input.close()
        if parsed_args.output:
            parsed_args.output.close()


if __name__ == "__main__":
    sys.exit(main())
