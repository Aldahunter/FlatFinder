import os
import typing
import unittest
import argparse

this_file = os.path.join(os.path.dirname(__file__), 'activate_this.py')
exec(open(this_file).read(), {'__file__': this_file})

class Args(argparse.Namespace):
    mode: str

def run() -> int:
    return os.system("python -m mypy .\FlatFinder.py")

def run_tests() -> int:
    start_dir = "."
    tests = unittest.defaultTestLoader.discover(start_dir, pattern = 'test*.py')
    runner = unittest.TextTestRunner()
    result = runner.run(tests)
    return len(result.errors) + len(result.failures)


parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['type-check', 'tests', 'both'], default='both')
args = typing.cast(Args, parser.parse_args())

error_code = 0
if args.mode in ['type-check', 'both']:
        error_code += run()
if args.mode in ['tests', 'both']:
    error_code += run_tests()
quit(error_code)