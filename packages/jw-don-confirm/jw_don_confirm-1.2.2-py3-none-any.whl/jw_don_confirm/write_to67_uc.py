import locale

from jw_don_confirm.services import MasterdataService, PDFService, AddressRepo, DonationsRepo
from jw_don_confirm.entities import YearlyDonations, Donation
from datetime import date
from jw_don_confirm.constants import Constants

import logging
import os

class WriteTO67UC:
    DATE_FORMAT = "%d.%m.%Y"
    NUMBER_FORMAT = "%.2f"
    LOCALE = "de_DE"
    LANGUAGE = "de"


    def __init__(self, masterdata: MasterdataService, pdf_filler_service: PDFService, address_repo: AddressRepo,
                 donations_repo: DonationsRepo):
        self.pdf_filler_service = pdf_filler_service
        self.masterdata = masterdata
        self.address_repo = address_repo
        self.donations_repo = donations_repo
        locale.setlocale(locale.LC_ALL, self.LOCALE)

    def _add_congregation_field(self, values: dict):
        values[Constants.CONGREGATION_NAME_FIELD] = self.masterdata.get_congregation_name()

    def _add_coordinator_field(self, values: dict):
        values[Constants.COORDINATOR_NAME_FIELD] = self.masterdata.get_coordinator()

    def _add_address_field(self, name: str, values: dict):
        address = self.address_repo.getAddress(name)
        if address is not None:
            values[Constants.ADDRESS_FIELD] = "\n" + name + "\n" + self.address_repo.getAddress(name)
        else:
            values[Constants.ADDRESS_FIELD] = "\n" + name
            logging.warning('No address found for name ' + name + '. No address written!')

    def _add_sum_in_words(self, yd: YearlyDonations, values: dict):
        values[Constants.SUM_IN_WORDS_FIELD] = yd.get_sum_as_word(self.LANGUAGE)

    def _add_sum(self, yd: YearlyDonations, values: dict):
        formated_value = locale.format_string(self.NUMBER_FORMAT, yd.get_sum())
        values[Constants.SUM_FIELD] = formated_value

    def _add_period(self, yd: YearlyDonations, values: dict):
        start = yd.getPeriod().start.strftime(self.DATE_FORMAT)
        end = yd.getPeriod().end.strftime(self.DATE_FORMAT)
        values[Constants.PERIOD_FIELD] = start + " - " + end

    def _add_place_date_sig(self, values: dict):
        today = date.today().strftime(WriteTO67UC.DATE_FORMAT)
        values[Constants.PLACE_DATE_SIG_FIELD] = self.masterdata.get_co_place() + ", " + today

    def _add_single_donation(self, donation: Donation, index: int, values: dict):
        formated_value = locale.format_string(self.NUMBER_FORMAT, donation.value)
        values[Constants.DONATION_VALUE_FIELD + str(index)] = formated_value
        values[Constants.DONATION_DATE_FIELD + str(index)] = donation.date.strftime(self.DATE_FORMAT)

    def write_page_one(self, name: str, input_pdf: str, output_pdf: str):
        content = {}
        yd = self.donations_repo.get_yearly_donations(name)
        self._add_congregation_field(content)
        self._add_coordinator_field(content)
        self._add_address_field(name, content)
        self._add_sum(yd, content)
        self._add_sum_in_words(yd, content)
        self._add_period(yd, content)
        self._add_place_date_sig(content)
        self.pdf_filler_service.fill_form(input_pdf, output_pdf, 0, content)

    def write_page_two(self, name: str, input_pdf: str, output_pdf: str):
        content = {}
        yd = self.donations_repo.get_yearly_donations(name)
        donations_list = yd.get_sorted_donations()

        for i, donation in enumerate(donations_list, start=1):
            self._add_single_donation(donation, i, content)

        self._add_sum(yd, content)
        self.pdf_filler_service.fill_form(input_pdf, output_pdf, 1, content)

    def create_all_confirmations(self, input_pdf: str, output_dir: str):
        for donator in self.donations_repo.get_donators():
            temp_pdf = os.path.join(output_dir, donator + "_temp")
            input_pdf_wo_ext = os.path.splitext(input_pdf)[0]
            output_pdf = os.path.basename(input_pdf_wo_ext) + "_" + donator + ".pdf"
            self.write_page_one(donator, input_pdf, temp_pdf)
            self.write_page_two(donator, temp_pdf, os.path.join(output_dir, output_pdf))
            os.remove(temp_pdf)
