import unittest


from pycompiler import Compiler
from pycompiler import Opcode
from pycompiler import Program



class AssignmentTest(unittest.TestCase):

    def setUp(self) -> None:
        self.compiler = Compiler()


    def test_assign_constant(self) -> None:

        source = """x = 5"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.STORE_NAME]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_double_assignment(self) -> None:

        source = """x = y = 5"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.DUO_TOP, Opcode.STORE_NAME, Opcode.STORE_NAME]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 1, "y": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


if __name__ == "__main__":
    unittest.main()