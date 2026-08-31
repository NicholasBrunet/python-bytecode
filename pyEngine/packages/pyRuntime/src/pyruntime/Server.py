from packages.pyRuntime.src.pyruntime.Account import Account
from pyruntime.VirtualMachine import VirtualMachine

class Server():

    __next_server_id__ = 0

    def __init__(self):

        self._server_id: int = Server.__next_server_id__
        self._accounts: dict[int, Account] = {}
        self._virtual_machines: dict[int, VirtualMachine] = {}

        self._index_account_virtual_machine: dict[int, int] = {}

        Server.__next_server_id__ += 1

    # def register_client(self, account: Account)

