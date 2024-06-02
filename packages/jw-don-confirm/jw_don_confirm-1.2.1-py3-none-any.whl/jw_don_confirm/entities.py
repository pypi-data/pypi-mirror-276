from num2words import num2words
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List


@dataclass
class Donation:
    value: Decimal  # The value in Euros
    date: date  # The date of the donation

    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = date.fromisoformat(self.date)


@dataclass
class DateRange:
    start: date
    end: date


@dataclass
class YearlyDonations:
    donations: dict[date, Donation] = None

    def __post_init__(self):
        if self.donations is None:
            self.donations = dict()  # set default value of donations

    def get_sorted_donations(self):
        # Check if donations exist
        if len(self.donations) == 0 :
            return []
        else:
            # Sort the donations list by 'date' attribute of the Donation objects
            donations_list = list(self.donations.values())
            donations_list.sort(key=lambda donation: donation.date)
            return donations_list


    def getPeriod(self) -> DateRange:
        if not self.donations:
            raise ValueError("Donations list is empty, so we can't provide a date range")
        #We take the the first donation's year and assume that this is the covered period
        year = list(self.donations.values())[0].date.year
        start = date(year, 1, 1)
        end = date(year, 12, 31)
        return DateRange(start, end)

    def get_sum_as_word(self, lang: str) -> str:
        total = self.get_sum()
        return num2words(total, lang=lang)

    def get_sum(self):
        total = Decimal(0)
        for donation in self.donations.values():
            total += donation.value
        return total

    def add_donation(self, donation: Donation):
        self.donations[donation.date] = donation
