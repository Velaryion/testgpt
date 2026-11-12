"""Expose test tracebacks as Actions annotations as well as console output."""
import sys
import unittest
suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(verbosity=2).run(suite)
for test, traceback in result.failures + result.errors:
    message = traceback.replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
    print(f'::error title={test.id()}::{message}', flush=True)
sys.exit(0 if result.wasSuccessful() else 1)
