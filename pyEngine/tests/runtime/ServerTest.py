import unittest

# from pycompiler import Opcode
from pycompiler import Compiler
from pyruntime import Account, Server

class ServerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.compiler = Compiler()
        self.compile = self.compiler.compile

        self.server = Server()
        self.account = Account()

        # Creates a virtual machine for account
        self.server.register_account(self.account)

        self.vm = self.server.vm_of(self.account.id)

    def test_execute_program(self) -> None:

        source = """x = 5
y = x - 5"""

        program = self.compile(source, True)
        program_id = self.vm.store_program(program)

        self.vm.execute_program(program_id)

if __name__ == "__main__":
    unittest.main()