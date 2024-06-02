from dataclasses import dataclass, field

from jw_don_confirm.json_data_repo import JsonDataRepo
from jw_don_confirm.services import AddressRepo


@dataclass
class AddressDict:
    addresses: dict[str, str] = field(default_factory=dict)


class JsonAddressRepo(AddressRepo, JsonDataRepo[AddressDict]):

    def addAddress(self, name: str, address: str):
        self.data.addresses[name] = address

    def getAddress(self, name: str) -> str:
        return self.data.addresses.get(name)

    def __init__(self, filename: str):
        super().__init__(filename, AddressDict)
