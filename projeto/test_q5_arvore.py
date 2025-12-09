import unittest
# Aqui fazemos a importação do arquivo de lógica
from q5_arvore import Tree, TreeNode

class TestGenericTree(unittest.TestCase):
    
    def setUp(self):
        """
        Configura o cenário de teste antes de cada método.
        """
        self.tree = Tree("CEO")
        
        # Nível 1
        self.cto = TreeNode("CTO")
        self.cfo = TreeNode("CFO")
        self.tree.root.add_child(self.cto)
        self.tree.root.add_child(self.cfo)

        # Nível 2
        self.dev = TreeNode("Lead Dev")
        self.qa = TreeNode("QA Manager")
        self.cto.add_child(self.dev)
        self.cto.add_child(self.qa)

        self.acc = TreeNode("Accountant")
        self.cfo.add_child(self.acc)

    def test_structure_integrity(self):
        """Testa se a hierarquia pai-filho foi estabelecida corretamente."""
        self.assertIn(self.cto, self.tree.root.children)
        self.assertIn(self.qa, self.cto.children)
        self.assertNotIn(self.qa, self.cfo.children)

    def test_find_root_element(self):
        """Testa a busca do elemento raiz."""
        found = self.tree.find("CEO")
        self.assertIsNotNone(found)
        self.assertEqual(found.data, "CEO")

    def test_find_deep_element(self):
        """Testa a busca de um elemento em níveis profundos (DFS)."""
        found = self.tree.find("Accountant")
        self.assertIsNotNone(found)
        self.assertEqual(found.data, "Accountant")

    def test_find_non_existent_element(self):
        """Testa se a busca retorna None para elementos inexistentes."""
        found = self.tree.find("Estagiario")
        self.assertIsNone(found)

if __name__ == '__main__':
    unittest.main()