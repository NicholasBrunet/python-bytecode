import unittest


from pycompiler import Compiler
from pycompiler import Opcode



class ImportTest(unittest.TestCase):

    def setUp(self) -> None:
        self.compiler = Compiler()
        self.compiler._available_globals = {
            "game.World": "World",
            "game": "game"
        }


    def test_single_import(self) -> None:

        source = """import game"""

        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"game": 0}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


    def test_multi_import(self) -> None:

        source = """import game, game.World"""

        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL, Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"game": 0, "game.World": 1}
        globals_generated = self.compiler._globals

        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


    def test_aliased_import(self) -> None:

        source = """import game as w"""


        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"game": 0, "w": 1}
        globals_generated = self.compiler._globals
        
        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)

    
    def test_deep_submodule_import(self) -> None:

        source = """import game.utils.math"""

        self.compiler._available_globals.update({"game.utils.math": len(self.compiler._available_globals)})

        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"game.utils.math": 0}
        globals_generated = self.compiler._globals
        
        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


    def test_deep_submodule_aliased_import(self) -> None:

        source = """import game.utils.math as gmath"""

        self.compiler._available_globals.update({"game.utils.math": len(self.compiler._available_globals)})

        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"gmath": 0}
        globals_generated = self.compiler._globals
        
        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


    def test_target_import(self) -> None:

        source = """from game import World"""

        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"World": 1, "game.World": 0}
        globals_generated = self.compiler._globals
        
        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


    def test_multi_target_import(self) -> None:

        source = """from game import World, Player"""

        self.compiler._available_globals.update({"game.Player": len(self.compiler._available_globals)})

        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL, Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"World": 1, "Player": 3, "game.Player": 2, "game.World": 0}
        globals_generated = self.compiler._globals
        
        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


    def test_target_aliased_import(self) -> None:

        source = """from game import World as w"""

        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"w": 1, "game.World": 0}
        globals_generated = self.compiler._globals
        
        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


    def test_deep_submodule_aliased_import(self) -> None:

        source = """from game.entities.drones import Drone as dro"""

        self.compiler._available_globals.update({"game.entities.drones.Drone": len(self.compiler._available_globals)})

        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"game.entities.drones.Drone": 0, "dro": 1}
        globals_generated = self.compiler._globals
        
        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)


    def test_multi_line_import(self) -> None:

        source = """
from game import (
    World,
    Player
)
"""

        self.compiler._available_globals.update({"game.Player": len(self.compiler._available_globals)})

        opcodes_expected = [Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL, Opcode.LOAD_GLOBAL, Opcode.STORE_GLOBAL]
        opcodes_generated = self.compiler.compile(source, True).opcodes

        globals_expected = {"World": 1, "Player": 3, "game.Player": 2, "game.World": 0}
        globals_generated = self.compiler._globals
        
        self.assertEqual(opcodes_expected, opcodes_generated)
        self.assertEqual(globals_expected, globals_generated)

    
    def test_wildcard_import(self) -> None:

        source = """from game import *"""

        with self.assertRaises(Exception):
            self.compiler.compile(source, True)

    
    def test_relative_import(self) -> None:

        source = """from . import game"""

        with self.assertRaises(ValueError):
            self.compiler.compile(source, True)

    
    def test_relative_parent_import(self) -> None:

        source = """from ..core import game"""

        with self.assertRaises(ValueError):
            self.compiler.compile(source, True)



if __name__ == "__main__":
    unittest.main()