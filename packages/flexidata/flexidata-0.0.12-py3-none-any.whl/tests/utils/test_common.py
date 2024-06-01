import unittest
from flexidata.utils.common import check_package_installed

class TestCommon(unittest.TestCase):
    def test_check_package_installed(self):
        with self.assertRaises(ImportError):
            check_package_installed("non_existent_package")

if __name__ == "__main__":
    unittest.main()
    