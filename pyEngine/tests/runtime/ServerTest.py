import unittest

# from pycompiler import Opcode
from pycompiler import Compiler, Opcode, Program
from pyruntime import Account, Server, VirtualMachine, ThreadPromise

class ServerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.compiler = Compiler()
        self.compile = self.compiler.compile

        self.server = Server()
        self.account = Account()

        # Creates a virtual machine for account
        self.server.register_account(self.account)

        self.vm: VirtualMachine = self.server.vm_of(self.account.id)

    def test_execute_program(self) -> None:

        source = \
"""
x = 6
y = x - 5
"""

        program = self.compile(source, True)
        program_id = self.vm.store_program(program)

        opcodes_expected = [
            Opcode.LOAD_CONST, 
            Opcode.STORE_GLOBAL, 
            Opcode.LOAD_GLOBAL, 
            Opcode.LOAD_CONST, 
            Opcode.BIN_SUB, 
            Opcode.STORE_GLOBAL
        ]
        self.assertEqual(opcodes_expected, program.opcodes)
        self.assertEqual(program, Program.of_binary(program.binary))

        thread_promise = self.vm.execute_program(program_id)

        while self.vm.tick():
            # pass
            print(thread_promise.thread)

if __name__ == "__main__":
    unittest.main()