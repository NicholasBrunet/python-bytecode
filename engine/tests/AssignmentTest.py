import unittest


from compiler.CompilerV2 import CompilerV2
from runtime.Opcode import Opcode



class AssignmentTest(unittest.TestCase):

    def setUp(self) -> None:
        self.compiler = CompilerV2()


    def test_assign_constant(self) -> None:

        source = """x = 5"""

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True)

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


    def test_assign_binary_addition(self) -> None:

        source = """x = 5 + 3"""

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.BIN_ADD, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True)

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


if __name__ == "__main__":
    unittest.main()