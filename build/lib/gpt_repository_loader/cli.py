import argparse
import os
import sys
from .loader import main

def parse_args():
    parser = argparse.ArgumentParser(description="Convert Git repository contents into a structured text format.")
    parser.add_argument("repo_path", nargs="?", default=".", help="Path to the Git repository (default: current directory)")
    parser.add_argument("-o", "--output", default="output.txt", help="Output file path (default: output.txt)")
    parser.add_argument("-p", "--preamble", help="Path to a preamble file (optional)")

    return parser.parse_args()

def main_cli():
    args = parse_args()

    # Convert "." to absolute path for Windows compatibility
    repo_path = os.path.abspath(args.repo_path)

    # Ensure the path is valid
    if not os.path.isdir(repo_path):
        print(f"Error: The specified repository path '{repo_path}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    main(repo_path, args.output, args.preamble)

if __name__ == "__main__":
    main_cli()
