
import json
import argparse

# Model-related functions
def update_docs(manifest, nodes_to_update):
    """
    Update the docs value for specified nodes.
    Set docs to true for specified nodes and false for all other nodes.
    """
    for node_name, node_info in manifest['nodes'].items():
        if node_name in nodes_to_update:
            node_info['docs']['show'] = True
        else:
            node_info['docs']['show'] = False

def true_docs(manifest):
    """
    Set the docs value for all nodes to true.
    """
    for node_name, node_info in manifest['nodes'].items():
        node_info['docs']['show'] = True

def false_docs(manifest):
    """
    Set the docs value for all nodes to false.
    """
    for node_name, node_info in manifest['nodes'].items():
        node_info['docs']['show'] = False

def list_models(manifest):
    """
    List all models in the manifest file.
    """
    for node_name in manifest['nodes']:
        print(node_name)

# Source-related functions
def remove_source(manifest, source_name_to_remove):
    """
    Remove a specified source from the manifest.
    """
    if source_name_to_remove in manifest.get('sources', {}):
        del manifest['sources'][source_name_to_remove]
        print(f"The source '{source_name_to_remove}' has been removed from the manifest file.")
    else:
        print(f"The source '{source_name_to_remove}' was not found in the manifest file.")

def remove_all_sources(manifest):
    """
    Remove all sources from the manifest.
    """
    manifest['sources'] = {}
    print("All sources have been removed from the manifest file.")

def list_sources(manifest):
    """
    List all sources in the manifest file.
    """
    source_names = list(manifest.get('sources', {}).keys())
    print("Available Sources:")
    for source_name in source_names:
        print("-", source_name)

# Macro-related functions
def update_docs_for_macros(manifest, macros_to_update):
    """
    Update the docs value for specified macros.
    Set docs to true for specified macros and false for all other macros.
    """
    for macro_name, macro_info in manifest['macros'].items():
        if macro_name in macros_to_update:
            macro_info['docs']['show'] = True
        else:
            macro_info['docs']['show'] = False

def true_docs_for_macros(manifest):
    """
    Set the docs value for all macros to true.
    """
    for macro_name, macro_info in manifest['macros'].items():
        macro_info['docs']['show'] = True

def false_docs_for_macros(manifest):
    """
    Set the docs value for all macros to false.
    """
    for macro_name, macro_info in manifest['macros'].items():
        macro_info['docs']['show'] = False

def list_macros(manifest):
    """
    List all macro package names in the manifest file.
    """
    packages = set()
    for macro_name in manifest['macros']:
        package_name = macro_name.split('.')[1]
        packages.add(package_name)
    for package in sorted(packages):
        print(f"macro.{package}")

# Main function to handle models, sources, and macros
def main(models, sources, macros, actions):
    # Load the manifest.json file
    print("Main Function Execution Begins...")
    with open('manifest.json', 'r') as file:
        manifest = json.load(file)

    # Handle model-related actions
    if 'model' in actions:
        if 'true-all' in models:
            true_docs(manifest)
        elif 'false-all' in models:
            false_docs(manifest)
        elif 'list' in models:
            list_models(manifest)
            return
        else:
            update_docs(manifest, models)

    # Handle source-related actions
    if 'source' in actions:
        if 'remove-all' in sources:
            remove_all_sources(manifest)
        elif 'list' in sources:
            list_sources(manifest)
            return
        else:
            for source in sources:
                remove_source(manifest, source)

    # Handle macro-related actions
    if 'macro' in actions:
        if 'true-all' in macros:
            true_docs_for_macros(manifest)
        elif 'false-all' in macros:
            false_docs_for_macros(manifest)
        elif 'list' in macros:
            list_macros(manifest)
            return
        else:
            update_docs_for_macros(manifest, macros)

    # Save the updated manifest.json file
    with open('manifest.json', 'w') as file:
        json.dump(manifest, file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage docs, sources, and macros in manifest.json.")
    parser.add_argument('actions', metavar='A', type=str, nargs='+',
                        help='Specify "model" to update model docs, "source" to update sources, or "macro" to update macros.')
    parser.add_argument('--model', metavar='M', type=str, nargs='*',
                        help='List of model names to update, "true-all" to set all docs values to true, "false-all" to set all docs values to false, or "list" to list all models')
    parser.add_argument('--source', metavar='S', type=str, nargs='*',
                        help='List of source names to remove, "remove-all" to remove all sources, or "list" to list all sources')
    parser.add_argument('--macro', metavar='M', type=str, nargs='*',
                        help='List of macro names to update, "true-all" to set all docs values to true, "false-all" to set all docs values to false, or "list" to list all macros')

    args = parser.parse_args()
    actions = args.actions
    models = args.model or []
    sources = args.source or []
    macros = args.macro or []

    main(models, sources, macros, actions)
