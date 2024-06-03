import unittest
from readme_ation.readme_generator import open_or_create_readme

class TestReadmeOperations(unittest.TestCase):

    def test_open_or_create_readme(self):
        content = open_or_create_readme('README.md')
        self.assertIsInstance(content, str)

if __name__ == '__main__':
    unittest.main()
