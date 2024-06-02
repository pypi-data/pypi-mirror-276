import logging
import os
import re
from datetime import date

import dateparser
from babel.numbers import parse_decimal

from jw_don_confirm.entities import Donation
from jw_don_confirm.services import MasterdataService, PDFService, DonationsRepo

DATE_LOCALE = 'de_DE'
DATE_IN_GIVER_NAME_REGEX = r"(.*)\((.*)\)"


class ReadFrom26UC:

    def __init__(self, masterdata: MasterdataService, pdf_service: PDFService,
                 donations_repo: DonationsRepo):
        self.pdf_service = pdf_service
        self.masterdata = masterdata
        self.donations_repo = donations_repo

    def read_month(self, input_pdf) -> date:
        # To get the month, it is better, to use the plain extraction mode
        text = self.pdf_service.extract_text(input_pdf, extraction_mode="plain")
        date_match = re.search(self.masterdata.get_date_regex_pattern(), text)
        if date_match:
            date_text = date_match.group(1)
            extracted_date: date = dateparser.parse(date_text).date()
            # Always return the first date of the month as reference date
            return extracted_date.replace(day=1)
        else:
            logging.debug(text)
            raise ValueError("Could not find date in: " + input_pdf)

    def read_donations(self, input_pdf):
        text: str = self.pdf_service.extract_text(input_pdf, "layout")
        logging.debug("Extracted Text for " + input_pdf + ":\n" + text)

        # Reading the current month
        try:
            month: date = self.read_month(input_pdf)
        except ValueError:
            logging.warning("No date found in file " + input_pdf + ". Ignoring this file.")
            return

        pattern = re.compile(self.masterdata.get_donation_regex_pattern(), re.MULTILINE)

        matches = pattern.findall(text)
        if len(matches) == 0:
            logging.warning("Could not find any donations in:" + input_pdf)

        for don_match in matches:
            donation_date = month.replace(day=int(don_match[0]))
            donation_giver = don_match[1].strip()
            donation_value = parse_decimal(don_match[2], locale=DATE_LOCALE)

            # If a specific date was given in brackets in the donation giver, we fix this now
            date_match = re.search(DATE_IN_GIVER_NAME_REGEX, donation_giver)
            if date_match:
                donation_giver = date_match.group(1).strip()
                donation_date = dateparser.parse(date_match.group(2)).date()

            self.donations_repo.add_donation(donation_giver, Donation(donation_value, donation_date))

    def read_donations_from_dir(self, input_dir):
        files = os.scandir(input_dir)
        for file in files:
            if file.is_file() and file.name.endswith(".pdf"):
                self.read_donations(file.path)
        self.donations_repo.persist()
