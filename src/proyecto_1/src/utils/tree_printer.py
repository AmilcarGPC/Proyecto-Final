from models.nodes import Node

class TreePrinter:
    @staticmethod
    def print_tree(root: Node):
        def _print_node(node: Node, prefix: str = "", is_last: bool = True):
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}[{node.type.value}] {node.content}")
            
            child_prefix = prefix + ("    " if is_last else "│   ")
            
            for i, child in enumerate(node.children):
                is_last_child = i == len(node.children) - 1
                _print_node(child, child_prefix, is_last_child)

        print("Python File Tree:")
        for i, child in enumerate(root.children):
            is_last = i == len(root.children) - 1
            _print_node(child, "", is_last)