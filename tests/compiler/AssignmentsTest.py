import unittest
import ast

from pvr.compiler import Compiler
from pvr.code import (
    CodeObject,
    LOAD_STR,
    LOAD_INT,
    LOAD_FLOAT,
    STORE_NAME,
    RETURN_VALUE
)

class AssignmentsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls): # runs once before all tests
        cls.compiler = Compiler()

    def setUp(self): # runs before each test
        self.module_1 = """
x = "5"
"""
        self.module_2 = """
x = 5
"""
        self.module_3 = """
x = 0.5
"""

    def test_primitive_str(self):
        ast_module = ast.parse(self.module_1, mode='exec')

        code_object = self.compiler.compile_module(ast_module, "test")

        expected_strs = ["5"]
        expected_opcodes = [LOAD_STR, 0, STORE_NAME, 0]

        self.assertListEqual(expected_strs, code_object.strs)
        self.assertListEqual(expected_opcodes, list(code_object.instructions))

    def test_primitive_int(self):
        ast_module = ast.parse(self.module_2, mode='exec')

        code_object = self.compiler.compile_module(ast_module, "test")

        expected_ints = [5]
        expected_opcodes = [LOAD_INT, 0, STORE_NAME, 0]

        self.assertListEqual(expected_ints, code_object.ints)
        self.assertListEqual(expected_opcodes, list(code_object.instructions))

    def test_primitive_float(self):
        ast_module = ast.parse(self.module_3, mode='exec')

        code_object = self.compiler.compile_module(ast_module, "test")

        expected_floats = [0.5]
        expected_opcodes = [LOAD_FLOAT, 0, STORE_NAME, 0]

        self.assertListEqual(expected_floats, code_object.floats)
        self.assertListEqual(expected_opcodes, list(code_object.instructions))

        print(code_object.floats)