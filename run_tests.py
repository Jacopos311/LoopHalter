import unittest
from pathlib import Path

if __name__ == "__main__":
    root = Path(__file__).parent
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(root / "tests"), pattern='test*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("\nRESULT: {} tests run.".format(result.testsRun))
    if result.wasSuccessful():
        print("STATUS: PASSED")
    else:
        print("STATUS: FAILED")
        print("Failures: {}".format(len(result.failures)))
        print("Errors: {}".format(len(result.errors)))
    raise SystemExit(not result.wasSuccessful())
