import abc
from typing import List, Literal

from jw_don_confirm.entities import YearlyDonations
from jw_don_confirm.entities import Donation


class PDFService(metaclass=abc.ABCMeta):
    """
    The interface to work with  PDFForms
    """

    @abc.abstractmethod
    def fill_form(self, input_pdf: str, output_pdf_str: str, page: int, content: dict):
        pass

    @abc.abstractmethod
    def read_form_field(self, input_pdf: str, field_name: str) -> str:
        pass

    @abc.abstractmethod
    def extract_text(self, input_pdf: str, extraction_mode: Literal["layout","plain"]) -> str:
        pass


class Persistable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def persist(self):
        pass


class MasterdataService(abc.ABC, Persistable):

    @abc.abstractmethod
    def get_congregation_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_coordinator(self) -> str:
        pass

    @abc.abstractmethod
    def get_co_place(self) -> str:
        pass

    @abc.abstractmethod
    def get_date_regex_pattern(self) -> str:
        pass

    @abc.abstractmethod
    def get_donation_regex_pattern(self) -> str:
        pass


class AddressRepo(abc.ABC, Persistable):

    @abc.abstractmethod
    def getAddress(self, name: str) -> str:
        pass

    @abc.abstractmethod
    def addAddress(self, name: str, address: str):
        pass


class DonationsRepo(abc.ABC, Persistable):

    @abc.abstractmethod
    def get_yearly_donations(self, name: str) -> YearlyDonations:
        pass

    @abc.abstractmethod
    def get_donators(self) -> List[str]:
        pass

    @abc.abstractmethod
    def add_donation(self, name: str, donation: Donation):
        pass
