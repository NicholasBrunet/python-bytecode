import unittest


from compiler.Compiler import Compiler
from compiler.bytecode.Opcode import Opcode
from compiler.bytecode.Program import Program



class ComparisonTest(unittest.TestCase):

    def setUp(self) -> None:
        self.compiler = Compiler()


    def test_assign_comparison(self) -> None:

        source = """x = 1 == 2"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.COMPARE_OP, Opcode.STORE_GLOBAL]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_assign_multiple_comparison(self) -> None:

        source = """x = 1 == 2 == 3"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.COMPARE_OP, Opcode.COMPARE_OP, Opcode.STORE_GLOBAL]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


if __name__ == "__main__":
    unittest.main()