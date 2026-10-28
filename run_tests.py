import sys
import unittest
import tests

if __name__ == '__main__':
    # Load the tests directly from the imported tests package
    suite = unittest.defaultTestLoader.loadTestsFromModule(tests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Explicitly exit with 1 if any tests failed or errored
    if not result.wasSuccessful():
        sys.exit(1)
