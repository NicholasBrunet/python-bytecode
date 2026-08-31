import unittest


from pycompiler import Compiler
from pycompiler import Opcode
from pycompiler import Program



class OperationsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.compiler = Compiler()


    def test_assign_binary_addition(self) -> None:

        source = """x = 5 + 3"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.BIN_ADD, Opcode.STORE_GLOBAL]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_assign_multiple_binary_additions(self) -> None:

        source = """x = 5 + 3 + 8"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [
            Opcode.LOAD_CONST, 
            Opcode.LOAD_CONST, 
            Opcode.BIN_ADD, 
            Opcode.LOAD_CONST, 
            Opcode.BIN_ADD, 
            Opcode.STORE_GLOBAL
        ]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_assign_binary_subtraction(self) -> None:

        source = """x = 5 - 3"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.BIN_SUB, Opcode.STORE_GLOBAL]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_assign_binary_multiplication(self) -> None:

        source = """x = 5 * 3"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.BIN_MULT, Opcode.STORE_GLOBAL]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_assign_binary_division(self) -> None:

        source = """x = 5 / 3"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.BIN_DIV, Opcode.STORE_GLOBAL]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_assign_mixed_precedence_mul_first(self) -> None:

        source = """x = 5 + 3 * 8"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [
            Opcode.LOAD_CONST,  # 5
            Opcode.LOAD_CONST,  # 3
            Opcode.LOAD_CONST,  # 8
            Opcode.BIN_MULT,    # 3 * 8
            Opcode.BIN_ADD,     # 5 + (3 * 8)
            Opcode.STORE_GLOBAL # x
        ]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_assign_mixed_precedence_parentheses(self) -> None:
        source = """x = (5 + 3) * 8"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [
            Opcode.LOAD_CONST,  # 5
            Opcode.LOAD_CONST,  # 3
            Opcode.BIN_ADD,     # 5 + 3
            Opcode.LOAD_CONST,  # 8
            Opcode.BIN_MULT,    # (5 + 3) * 8
            Opcode.STORE_GLOBAL # x
        ]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_assign_complex_chain_mixed_operators(self) -> None:
        source = """x = 12 / 4 - 2 * 3"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [
            Opcode.LOAD_CONST,  # 12
            Opcode.LOAD_CONST,  # 4
            Opcode.BIN_DIV,     # 12 / 4
            Opcode.LOAD_CONST,  # 2
            Opcode.LOAD_CONST,  # 3
            Opcode.BIN_MULT,    # 2 * 3
            Opcode.BIN_SUB,     # (12 / 4) - (2 * 3)
            Opcode.STORE_GLOBAL # x
        ]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_assign_multiple_variables_tracking(self) -> None:
        source = """
x = 5 + 2
y = 10 - 4
"""
        program = self.compiler.compile(source, True)
        opcodes_expected = [
            Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.BIN_ADD, Opcode.STORE_GLOBAL, # x = 5 + 2
            Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.BIN_SUB, Opcode.STORE_GLOBAL  # y = 10 - 4
        ]
        opcodes_generated = program.opcodes

        globals_expected = {"x": 0, "y": 1}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))


    def test_binary_operation_with_call(self) -> None:
        source = """
xfassfasfasf = 5 + 2
y = xfassfasfasf - 4
"""
        program = self.compiler.compile(source, True)

        opcodes_expected = [
            Opcode.LOAD_CONST, Opcode.LOAD_CONST, Opcode.BIN_ADD, Opcode.STORE_GLOBAL,
            Opcode.LOAD_GLOBAL, Opcode.LOAD_CONST, Opcode.BIN_SUB, Opcode.STORE_GLOBAL
        ]
        opcodes_generated = program.opcodes

        globals_expected = {"xfassfasfasf": 0, "y": 1}
        globals_generated = self.compiler._globals

        print(f"Binary output: {program.binary}")
        # print(program)

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)
        self.assertEqual(program, Program.of_binary(program.binary))



if __name__ == "__main__":
    unittest.main()