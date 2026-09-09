import sys
import unittest
from collections import Counter, defaultdict


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


class PrettyResult(unittest.TextTestResult):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = defaultdict(list)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.groups[test.__class__.__name__].append((test._testMethodName, "PASS"))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.groups[test.__class__.__name__].append((test._testMethodName, "FAIL"))

    def addError(self, test, err):
        super().addError(test, err)
        self.groups[test.__class__.__name__].append((test._testMethodName, "ERROR"))


class PrettyRunner(unittest.TextTestRunner):

    resultclass = PrettyResult

    def run(self, test):
        result = super().run(test)
        print()

        for group, tests in result.groups.items():
            passed = sum(status == "PASS" for _, status in tests)
            total = len(tests)
            group_color = GREEN if passed == total else RED

            print(f"{group_color}{group} [{passed}/{total} passed]{RESET}")

            name_counts = Counter(name for name, _ in tests)
            name_indexes = defaultdict(int)

            for name, status in tests:
                display_name = name
                if name_counts[name] > 1:
                    name_indexes[name] += 1
                    display_name = f"{name} #{name_indexes[name]}"

                status_color = {
                    "PASS": GREEN,
                    "FAIL": RED,
                    "ERROR": YELLOW,
                }[status]

                symbol = {
                    "PASS": "✓",
                    "FAIL": "✗",
                    "ERROR": "!",
                }[status]

                print(f"  - {display_name}: {status_color}{symbol} {status}{RESET}")

            print()

        return result


suite = unittest.defaultTestLoader.discover(
    "./tests/compiler/",
    pattern="*Test.py",
)

PrettyRunner(
    verbosity=0,
).run(suite)
