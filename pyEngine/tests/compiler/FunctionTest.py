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
def func(a):
    return a
"""
#         source = """
# class func():
#     pass
# """
        program = self.compiler.compile(source, True)

        print(dis.dis(source))
        print(program)


if __name__ == "__main__":
    unittest.main()