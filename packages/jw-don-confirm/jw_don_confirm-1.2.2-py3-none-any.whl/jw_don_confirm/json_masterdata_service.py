from dataclasses import dataclass

from jw_don_confirm.json_data_repo import JsonDataRepo
from jw_don_confirm.services import MasterdataService


@dataclass
class Masterdata:
    congregation: str = ""
    coordinator: str = ""
    co_place: str = ""
    date_regex_pattern: str = r"\(\d*\)\s*(.*?\d{4}).*"
    donation_regex_pattern: str = r"^\s*(\d{2})(?!.*Branch.*).*-\s*(.*?)\s*CE\s*(\d{1,3}(.\d{3})*,\d*)$"


class JsonMasterdataService(MasterdataService, JsonDataRepo[Masterdata]):

    def __init__(self, filename: str):
        super().__init__(filename, Masterdata)

    def get_date_regex_pattern(self) -> str:
        return self.data.date_regex_pattern

    def get_coordinator(self) -> str:
        return self.data.coordinator

    def get_congregation_name(self) -> str:
        return self.data.congregation

    def get_co_place(self) -> str:
        return self.data.co_place

    def get_donation_regex_pattern(self) -> str:
        return self.data.donation_regex_pattern
