from typing import Any

class Account():

    __default_attributes__: dict[str, Any] = {
        "max_programs": 3,
        "api_acccess": {

        }
    }
    __next_server_id__ = 0

    def __init__(self, attributes: dict[str, Any] = {}):

        self._server_id: int = Account.__next_server_id__
        self._attributes: dict[str, Any] = dict(self.__default_attributes__) | attributes

        Account.__next_server_id__ += 1

    @property
    def id(self) -> int:
        return self._server_id

    @property
    def attributes(self) -> dict[str, Any]:
        return self._attributes

    @property
    def api_access(self) -> dict[str, Any]:
        return self._attributes["api_acccess"]
