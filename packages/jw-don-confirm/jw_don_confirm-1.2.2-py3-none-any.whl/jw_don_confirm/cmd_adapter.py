import argparse
import logging
from importlib.metadata import version
from jw_don_confirm.json_address_repo import JsonAddressRepo
from jw_don_confirm.json_donations_repo import JsonDonationsRepo
from jw_don_confirm.py_pdf_adapter import PyPDFAdapter
from jw_don_confirm.read_from67_uc import ReadFrom67UC
from jw_don_confirm.read_from26_uc import ReadFrom26UC
from jw_don_confirm.write_to67_uc import WriteTO67UC
from jw_don_confirm.services import AddressRepo
from jw_don_confirm.services import PDFService, DonationsRepo, MasterdataService

from jw_don_confirm.json_masterdata_service import JsonMasterdataService

MODE_ADDRESSES = "addresses"
MODE_DONATIONS = "donations"
MODE_CONFIRMATIONS = "confirmations"


def main():
    paket_version = version("jw_don_confirm")

    parser = argparse.ArgumentParser(description="A programm to generate donation confirmations for congregations "
                                                 "Jehovah's Witnesses in Germany. Version: " + paket_version)
    #Debug Mode
    parser.add_argument("--debug", action="store_true",
                        help="set log level to DEBUG")

    # Mode Parameter
    parser.add_argument('--mode', choices=[MODE_ADDRESSES, MODE_DONATIONS, MODE_CONFIRMATIONS])

    # The working directory
    parser.add_argument('--dir', required=True,
                        help='The working directory')

    # The file for addresses
    parser.add_argument('--addressfile', default='./data/addresses.json',
                        help='The JSON file used for reading and writing addresses')

    # The file for donations
    parser.add_argument('--donationsfile', default='./data/donations.json',
                        help='The JSON file used for reading and writing donations')

    # The file for masterdata
    parser.add_argument('--masterdatafile', default='./data/masterdata.json',
                        help='The JSON file used for reading masterdata')

    # The file for masterdata
    parser.add_argument('--inputpdf',
                        help='The input pdf for creating donation')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)

    # Now Setup the services
    pdf_service: PDFService = PyPDFAdapter()
    address_repo: AddressRepo = JsonAddressRepo(args.addressfile)
    donations_repo: DonationsRepo = JsonDonationsRepo(args.donationsfile)
    masterdata: MasterdataService = JsonMasterdataService(args.masterdatafile)

    # Persist the masterdata file, so that we have at least an empty file for editing
    masterdata.persist()

    if args.mode == MODE_ADDRESSES:
        uc = ReadFrom67UC(pdf_service, address_repo)
        uc.read_addresses_from_dir(args.dir)

    if args.mode == MODE_DONATIONS:
        uc = ReadFrom26UC(masterdata, pdf_service, donations_repo)
        uc.read_donations_from_dir(args.dir)

    if args.mode == MODE_CONFIRMATIONS:
        if args.inputpdf is None:
            parser.error('For writing donation confirmations the parameter inputpdf is neccessary.')
        uc = WriteTO67UC(masterdata, pdf_service, address_repo, donations_repo)
        uc.create_all_confirmations(args.inputpdf, args.dir)

if __name__ == "__main__":
    main()
