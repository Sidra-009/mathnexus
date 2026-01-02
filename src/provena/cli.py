"""
Command-line interface for Provena.
"""

import sys
import json
import argparse
from typing import List
from .logger import ProvenaLogger
from .reporter import generate_terminal_report, generate_json_report

def main(args: List[str] = None):
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Provena - Audit trail system for data transformations",
        prog="provena"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate audit report")
    report_parser.add_argument("json_file", help="Input JSON audit file")
    report_parser.add_argument("--format", choices=["terminal", "json"], 
                              default="terminal", help="Output format")
    report_parser.add_argument("-o", "--output", help="Output file (for JSON format)")
    
    # Version command
    subparsers.add_parser("version", help="Show version")
    
    # Parse arguments
    parsed_args = parser.parse_args(args)
    
    if parsed_args.command == "version":
        from . import __version__
        print(f"Provena v{__version__}")
        return 0
    
    elif parsed_args.command == "report":
        try:
            with open(parsed_args.json_file, 'r', encoding='utf-8') as f:
                audit_data = json.load(f)
            
            # Reconstruct logger from JSON
            logger = ProvenaLogger(audit_data.get("pipeline", "Unknown"))
            
            # Recreate records (simplified - in reality you'd need proper deserialization)
            print("Note: Full CLI reconstruction from JSON requires additional implementation.")
            print("For now, use the Python API directly.")
            
            if parsed_args.format == "terminal":
                print(generate_terminal_report(logger))
            elif parsed_args.format == "json":
                result = generate_json_report(logger, parsed_args.output)
                if not parsed_args.output:
                    print(result)
            
            return 0
            
        except FileNotFoundError:
            print(f"Error: File '{parsed_args.json_file}' not found.", file=sys.stderr)
            return 1
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in '{parsed_args.json_file}'.", file=sys.stderr)
            return 1
    
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())