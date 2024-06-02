import unittest
import pkg_vers

class TestUtils(unittest.TestCase):

    def test_find_all_py_files(self):
        files = pkg_vers.find_all_py_files('tests')
        self.assertIsInstance(files, list)

    def test_get_imported_top_level_packages(self):
        files = pkg_vers.find_all_py_files('tests')
        packages = pkg_vers.get_imported_top_level_packages(files)
        self.assertIsInstance(packages, list)

if __name__ == '__main__':
    unittest.main()
