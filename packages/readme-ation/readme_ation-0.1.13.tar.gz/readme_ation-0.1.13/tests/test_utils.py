import unittest
from readme_ation.utils import find_all_py_files, get_imported_packages

class TestUtils(unittest.TestCase):

    def test_find_all_py_files(self):
        files = find_all_py_files('tests')
        self.assertIsInstance(files, list)

    def test_get_imported_packages(self):
        files = find_all_py_files('tests')
        packages = get_imported_packages(files)
        self.assertIsInstance(packages, list)

if __name__ == '__main__':
    unittest.main()
