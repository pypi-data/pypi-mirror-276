from dataclasses import dataclass, field
from typing import List

from jw_don_confirm.json_data_repo import JsonDataRepo
from jw_don_confirm.services import DonationsRepo
from jw_don_confirm.entities import YearlyDonations, Donation


@dataclass
class DonationsDict:
    donations: dict[str, YearlyDonations] = field(default_factory=dict)


class JsonDonationsRepo(DonationsRepo, JsonDataRepo[DonationsDict]):

    def __init__(self, filename: str):
        super().__init__(filename, DonationsDict)

    def get_donators(self) -> List[str]:
        return list(self.data.donations.keys())

    def get_yearly_donations(self, name: str) -> YearlyDonations:
        return self.data.donations.get(name)

    def add_donation(self, name: str, donation: Donation):
        yd: YearlyDonations = self.get_yearly_donations(name)
        if not yd:
            # No donation entered so far
            yd = YearlyDonations()
            self.data.donations[name] = yd
        yd.add_donation(donation)
