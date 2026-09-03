import json
import unittest

from pycompiler import Compiler
from pycompiler import Opcode
from pycompiler import Program

import dis



class FunctionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.compiler = Compiler()


    def test_assign_comparison(self) -> None:

#         source = """
# def add(a: int, b: int) -> int:
#     return a + b
# """
        source = """
def func(a, b):
    return a + b

print(func(1, 2))
"""
#         source = """
# class func():
#     pass
# """
        program = self.compiler.compile(source, True)

        print(dis.dis(source))
        print(json.dumps([instruction.__str__() for instruction in program.instructions], indent=4))


if __name__ == "__main__":
    unittest.main()