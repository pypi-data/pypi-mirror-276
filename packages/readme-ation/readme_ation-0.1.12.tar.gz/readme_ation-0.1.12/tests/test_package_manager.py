import unittest
from readme_generator.package_manager import get_installed_packages, get_specific_packages_versions

class TestPackageManager(unittest.TestCase):

    def test_get_installed_packages(self):
        packages = get_installed_packages()
        self.assertIsInstance(packages, dict)

    def test_get_specific_packages_versions(self):
        versions = get_specific_packages_versions(['os', 'sys'], {'os': '1.0', 'sys': '2.0'})
        self.assertIsInstance(versions, dict)

if __name__ == '__main__':
    unittest.main()
