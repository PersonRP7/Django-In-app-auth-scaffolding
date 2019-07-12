import sys
sys.path.append("..")
import unittest
import test_auth_settings
import test_auth
import test_create_py_files
import test_models_in_app
import test_proceed

loader = unittest.TestLoader()
suite = unittest.TestSuite()

all_tests = [
    test_auth_settings,
    test_auth,
    test_create_py_files,
    test_models_in_app,
    test_proceed
]

for test in all_tests:
    suite.addTest(loader.loadTestsFromModule(test))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
