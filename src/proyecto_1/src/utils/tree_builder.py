from models.nodes import Node, NodeType
from typing import List

from utils.node_analyzer import NodeTypeAnalyzer

class TreeBuilder:
    def __init__(self):
        self.type_analyzer = NodeTypeAnalyzer()

    def build(self, lines: List[str]) -> Node:
        root = Node(NodeType.ROOT, "root", -1)
        current_parent = root
        indent_stack = [(root, -1)]
        
        for line in lines:
            if not line.strip():
                continue
                
            indent = len(line) - len(line.lstrip())
            node_type = self.type_analyzer.get_node_type(line)
            new_node = Node(node_type, line.strip(), indent)

            while indent_stack and indent <= indent_stack[-1][1]:
                indent_stack.pop()
                if indent_stack:
                    current_parent = indent_stack[-1][0]

            current_parent.add_child(new_node)
            
            if self._can_have_children(node_type):
                current_parent = new_node
                indent_stack.append((new_node, indent))

        return root

    def _can_have_children(self, node_type: NodeType) -> bool:
        return node_type in {
            NodeType.FUNCTION, NodeType.CLASS, NodeType.METHOD,
            NodeType.IF, NodeType.ELIF, NodeType.ELSE, 
            NodeType.FOR, NodeType.WHILE, NodeType.MATCH, NodeType.CASE
        }