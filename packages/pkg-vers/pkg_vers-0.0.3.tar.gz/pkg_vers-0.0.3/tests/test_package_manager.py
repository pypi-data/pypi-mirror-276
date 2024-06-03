import unittest
import pkg_vers

class TestPackageManager(unittest.TestCase):

    def test_get_installed_packages(self):
        packages = pkg_vers.get_installed_packages()
        self.assertIsInstance(packages, dict)

    def test_get_specific_package_versions(self):
        versions = pkg_vers.get_specific_package_versions(['os', 'sys'], {'os': '1.0', 'sys': '2.0'})
        self.assertIsInstance(versions, dict)

    def test_get_imported_top_level_packages(self):
        imported_packages = pkg_vers.get_imported_top_level_packages([__file__])
        self.assertIsInstance(imported_packages, list)

if __name__ == '__main__':
    unittest.main()
