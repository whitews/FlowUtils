import sys
import unittest

if __name__ == '__main__':
    # Discover and run all tests in the 'tests' directory
    suite = unittest.defaultTestLoader.discover('tests')
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Force a non-zero exit code if tests failed or raised errors
    if not result.wasSuccessful():
        sys.exit(1)
