from models.nodes import Node, NodeType
from utils.tree_printer import TreePrinter
from utils.tree_builder import TreeBuilder

class PythonFileTree:
    def __init__(self, file_content: str):
        self.builder = TreeBuilder()
        self.root = self.builder.build(file_content.splitlines())

    def print_tree(self):
        TreePrinter.print_tree(self.root)

    def count_logical_lines(self) -> int:
        logical_types = {
            NodeType.FUNCTION, NodeType.CLASS, 
            NodeType.IF, NodeType.ELIF, NodeType.ELSE,
            NodeType.FOR, NodeType.WHILE, 
            NodeType.MATCH, NodeType.CASE,
            NodeType.ASSIGNMENT
        }
        
        def traverse(node: Node) -> int:
            count = 1 if node.type in logical_types else 0
            return count + sum(traverse(child) for child in node.children)
            
        return traverse(self.root)