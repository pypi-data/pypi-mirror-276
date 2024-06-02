from typing import Literal

from jw_don_confirm.services import PDFService
from pypdf import PdfReader, PdfWriter


class PyPDFAdapter(PDFService):
    def read_form_field(self, input_pdf: str, field_name: str) -> str:
        reader = PdfReader(input_pdf)
        fields = reader.get_form_text_fields()
        return fields.get(field_name)

    def fill_form(self, input_pdf: str, output_pdf: str, page: int, content: dict):
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        writer.append(reader)
        page = writer.pages[page]
        writer.update_page_form_field_values(
            page,
            content,
            auto_regenerate=True,
        )

        # write "output" to pypdf-output.pdf
        with open(output_pdf, "wb") as output_stream:
            writer.write(output_stream)

    def extract_text(self, input_pdf: str, extraction_mode: Literal["layout","plain"]="layout") -> str:
        extracted_text: str = ""
        reader = PdfReader(input_pdf)
        for page in reader.pages:
            extracted_text += "\n" + page.extract_text(extraction_mode=extraction_mode, layout_mode_space_vertically=False)

        return extracted_text
