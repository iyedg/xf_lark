from rich.console import Console
from rich.tree import Tree


def normalize_quotes(text: str) -> str:
    replacements = {"‘": "'", "’": "'", "“": '"', "”": '"'}
    for find, replace in replacements.items():
        text = text.replace(find, replace)
    return text


def format_node_label(node_data):
    """Helper to create a label for a tree node from its dictionary representation."""
    if not isinstance(node_data, dict):
        return f"[cyan]{str(node_data)}[/cyan]"

    node_type = node_data.get("type", "Unknown_Node")
    label = f"[bold blue]{node_type}[/bold blue]"

    if "operator" in node_data:
        label += f" [purple]({node_data['operator']})[/purple]"
    if "name" in node_data:
        label += f" [green]'{node_data['name']}'[/green]"
    if "value" in node_data:
        label += f": [yellow]{repr(node_data['value'])}[/yellow]"

    return label


def add_ast_to_rich_tree(branch: Tree, ast_node):
    """
    Recursively adds nodes from the AST dictionary to a Rich Tree.
    """
    if isinstance(ast_node, dict):
        # For dictionary nodes, create a new branch with a label derived from the node's content
        current_branch = branch.add(format_node_label(ast_node))

        # Iterate over keys that might contain children, like 'left', 'right', 'operand', 'arguments'
        # Prioritize common structural keys for clearer hierarchy.
        children_keys = [
            "operand",
            "left",
            "right",
            "arguments",
        ]  # Order can matter for display

        processed_keys = set(
            ["type", "operator", "name", "value"]
        )  # Keys already used in label

        for key in children_keys:
            if key in ast_node:
                add_ast_to_rich_tree(current_branch, ast_node[key])
                processed_keys.add(key)

        # Add any other remaining dictionary items that haven't been processed
        # and are not part of the main label.
        for key, value in ast_node.items():
            if key not in processed_keys:
                child_branch = current_branch.add(f"[dim]{key}:[/dim]")
                add_ast_to_rich_tree(child_branch, value)

    elif isinstance(ast_node, list):
        # For lists (like function arguments), add each item as a child node
        # If the list is empty, you might want to indicate that.
        if not ast_node:
            branch.add("[dim]empty list[/dim]")
        else:
            for i, item in enumerate(ast_node):
                # Create a sub-branch for each item in the list
                item_branch = branch.add(f"[dim]item {i}:[/dim]")
                add_ast_to_rich_tree(item_branch, item)
    else:
        # For literal values, add them directly as a leaf
        branch.add(f"[cyan]{str(ast_node)}[/cyan]")


def display_ast_as_tree(ast_dict, title="AST"):
    """
    Displays the AST dictionary as a tree using Rich.
    """
    if not ast_dict:
        print("AST is empty or None.")
        return

    # The root of the tree will represent the initial AST dictionary
    tree_root_label = format_node_label(ast_dict)
    tree = Tree(tree_root_label)

    # Process children of the root node, skipping keys already in the root label
    processed_keys_for_root = set(["type", "operator", "name", "value"])
    children_keys = ["operand", "left", "right", "arguments"]

    for key in children_keys:
        if key in ast_dict:
            add_ast_to_rich_tree(tree, ast_dict[key])
            processed_keys_for_root.add(key)

    for key, value in ast_dict.items():
        if key not in processed_keys_for_root:
            child_branch = tree.add(f"[dim]{key}:[/dim]")
            add_ast_to_rich_tree(child_branch, value)

    console = Console()
    console.print(tree)
