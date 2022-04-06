from os import path, system
from typing import cast
from unittest import TestSuite, TextTestRunner, TestResult, defaultTestLoader
from argparse import ArgumentParser, Namespace

this_file: str = path.join(path.dirname(__file__), 'activate_this.py')
this_file_dict: dict[str, str] = {'__file__': this_file}
exec(open(this_file).read(), this_file_dict)

class Args(Namespace):
    mode: str

def run() -> int:
    return system("python -m mypy .\FlatFinder.py")

def run_tests() -> int:
    start_dir: str = "."
    tests: TestSuite = defaultTestLoader.discover(start_dir, pattern = 'test*.py')
    runner: TextTestRunner = TextTestRunner()
    result: TestResult = runner.run(tests)
    return len(result.errors) + len(result.failures)


parser: ArgumentParser = ArgumentParser()
parser.add_argument('--mode', choices=['type-check', 'tests', 'both'], default='both')
args: Args = cast(Args, parser.parse_args())

error_code: int = 0
if args.mode in ['type-check', 'both']:
        error_code += run()
if args.mode in ['tests', 'both']:
    error_code += run_tests()
quit(error_code)