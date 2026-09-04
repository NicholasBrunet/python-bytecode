import json
import unittest

from pycompiler import Compiler
from pycompiler import Opcode

import dis



class ConditionalsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.compiler = Compiler()


    def test_assign_comparison(self) -> None:

        source = """
a = 3
b = 4
if a != b:
    x = 10
elif a > b:
    x = 5
else:
    x = 1
"""
        code_object = self.compiler.compile(source, True)
        print(code_object.__repr__())

        print(dis.dis(source))
        # print(json.dumps([instruction.__str__() for instruction in code_object.instructions], indent=4))


if __name__ == "__main__":
    unittest.main()