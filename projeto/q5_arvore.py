from typing import List, Optional, Any

class TreeNode:
    """
    Representa um nó em uma estrutura de dados de Árvore N-ária.
    """
    def __init__(self, data: Any):
        self.data = data
        self.children: List['TreeNode'] = []

    def add_child(self, child_node: 'TreeNode') -> None:
        self.children.append(child_node)

    def find(self, target_data: Any) -> Optional['TreeNode']:
        if self.data == target_data:
            return self

        for child in self.children:
            result = child.find(target_data)
            if result:
                return result
        return None

    def __repr__(self) -> str:
        return f"TreeNode(data={self.data}, children={len(self.children)})"

class Tree:
    """
    Classe wrapper para a estrutura de árvore, contendo a raiz.
    """
    def __init__(self, root_data: Any):
        self.root = TreeNode(root_data)

    def find(self, data: Any) -> Optional[TreeNode]:
        return self.root.find(data)