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
        program = self.compiler.compile(source, True)

        opcodes_expected = [
            Opcode.LOAD_CONST, 
            Opcode.LOAD_CONST, 
            Opcode.COMPARE_OP, 
            Opcode.LOAD_CONST, 
            Opcode.COMPARE_OP, 
            Opcode.STORE_GLOBAL
        ]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        print(dis.dis(source))

        # self.assertEqual(opcodes_expected, opcodes_generated)
        # self.assertEqual(globals_expected, globals_generated)
        # self.assertEqual(program, Program.of_binary(program.binary))


if __name__ == "__main__":
    unittest.main()