import argparse
from .main import main  # Assuming your main function is defined in main.py

def parse_arguments():
    parser = argparse.ArgumentParser(description="Manage docs, sources, and macros in manifest.json.")
    parser.add_argument('actions', metavar='A', type=str, nargs='+',
                        help='Specify "model" to update model docs, "source" to update sources, or "macro" to update macros.')
    parser.add_argument('--model', metavar='M', type=str, nargs='*',
                        help='List of model names to update, "true-all" to set all docs values to true, "false-all" to set all docs values to false, or "list" to list all models')
    parser.add_argument('--source', metavar='S', type=str, nargs='*',
                        help='List of source names to remove, "remove-all" to remove all sources, or "list" to list all sources')
    parser.add_argument('--macro', metavar='M', type=str, nargs='*',
                        help='List of macro names to update, "true-all" to set all docs values to true, "false-all" to set all docs values to false, or "list" to list all macros')

    return parser.parse_args()

def main_wrapper():
    args = parse_arguments()
    main(args.model or [], args.source or [], args.macro or [], args.actions)

if __name__ == "__main__":
    main_wrapper()
