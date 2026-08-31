from .Account import Account
from .VirtualMachine import VirtualMachine

class Server():

    __next_server_id__ = 0

    def __init__(self):

        self._server_id: int = Server.__next_server_id__
        self._accounts: dict[int, Account] = {}
        self._virtual_machines: dict[int, VirtualMachine] = {}

        self._index_account_virtual_machine: dict[int, int] = {}

        Server.__next_server_id__ += 1

    @property
    def accounts(self) -> dict[int, Account]:
        return self._accounts
    
    @property
    def vms(self) -> dict[int, VirtualMachine]:
        return self._virtual_machines

    def register_account(self, account: Account):
        if account.id in self.accounts: raise KeyError(f"Server accounts already contains account id: {account.id}")

        vm: VirtualMachine = VirtualMachine(account.api_access)

        self._accounts[account.id] = account
        self._virtual_machines[vm.id] = vm
        self._index_account_virtual_machine[account.id] = vm.id

    def account_of(self, account_id: int) -> Account:
        if account_id not in self.accounts: raise KeyError(f"Server accounts does not contain account id: {account_id}")
        return self.accounts[account_id]

    def vm_of(self, account_id: int) -> VirtualMachine:
        if account_id not in self._index_account_virtual_machine: raise KeyError(f"Account with id: {account_id}, does not have a VirtualMachine")
        return self.vms[self._index_account_virtual_machine[account_id]]

