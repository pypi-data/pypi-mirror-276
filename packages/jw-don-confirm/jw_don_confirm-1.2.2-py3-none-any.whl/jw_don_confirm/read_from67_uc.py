import os
import re
from typing import Tuple

from jw_don_confirm.services import PDFService, AddressRepo
from jw_don_confirm.constants import Constants


class ReadFrom67UC:

    def __init__(self, pdf_service: PDFService, address_repo: AddressRepo):
        self.pdf_service = pdf_service
        self.address_repo = address_repo

    def read_address_from_pdf(self, input_pdf: str) -> Tuple[str, str]:
        address_field = self.pdf_service.read_form_field(input_pdf, Constants.ADDRESS_FIELD)

        #Might be empty
        if address_field is None:
            return None, None

        address_lines = re.split('[,\n]', address_field)
        name: str = ""
        address: str = ""
        for line in address_lines:
            striped_line = line.strip()
            # Check first, if we have an empty line
            if striped_line:
                if name == "":
                    # First none empty line is the name
                    name = striped_line
                elif address == "":
                    # Second none empty line is the first address line
                    address = striped_line
                else:
                    address = address + "\n" + striped_line

        return name, address

    def read_addresses_from_dir(self, input_dir: str):
        files = os.scandir(input_dir)
        for file in files:
            if os.path.isfile(file.path) and file.name.endswith(".pdf"):
                name, address = self.read_address_from_pdf(file.path)
                if name is not None:
                    self.address_repo.addAddress(name, address)
        self.address_repo.persist()
