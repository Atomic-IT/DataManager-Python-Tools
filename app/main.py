from fastapi import FastAPI, UploadFile
from enum import Enum
from pandas import DataFrame
from typing import Callable
from docx import Document
from odf.opendocument import OpenDocumentText
from odf.table import Table, TableRow, TableCell
import tabula


def from_odt(file):
    # Load the ODT document
    doc = OpenDocumentText(file)

    # Iterate through the tables in the document
    for table in doc.getElementsByType(Table):
        for row in table.getElementsByType(TableRow):
            # Extract text from each cell in the row
            row_data = []
            for cell in row.getElementsByType(TableCell):
                # Get the text content of the cell
                cell_text = "".join(
                    node.data
                    for node in cell.childNodes
                    if node.nodeType == node.TEXT_NODE
                )
                row_data.append(cell_text)
            print(row_data)  # Print or process the row data as needed


def from_pdf(file_path):
    # Read tables from the PDF file
    tables = tabula.read_pdf(file_path, pages="all", multiple_tables=True)

    # Iterate through the extracted tables
    for i, table in enumerate(tables):
        print(f"Table {i + 1}:")
        print(table)  # Print or process the table as needed


app = FastAPI()


class Formats(Enum):
    CSV = "csv"
    XML = "xml"
    JSON = "json"
    PDF = "pdf"


class ValidExtensions(Enum):
    CSV = "csv"
    XML = "xml"
    JSON = "json"
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    ODT = "odt"


FUNCTIONS: dict[Formats, Callable[[DataFrame], str]] = {
    Formats.CSV: lambda x: x.to_csv(),
    Formats.JSON: lambda x: x.to_json(),
    Formats.XML: lambda x: x.to_xml(),
}


def from_docx(file):
    # Load the document
    doc = Document(file)

    # Iterate through the tables in the document
    for table in doc.tables:
        for row in table.rows:
            # Extract text from each cell in the row
            row_data = [cell.text for cell in row.cells]


@app.post("/")
def transform(format: Formats, file: UploadFile):
    """
    Transforms given file to another format
    Parameters
    ----------
    format:
        Destination format to use
    file:
        File to transform. Requires valid extension
    """
    extension = file.filename.split(".")[-1]
    if extension in {"csv", "xml", "json"}:
        data = file.file.readlines()
        df = DataFrame(data[1:], columns=data[0])
    elif extension in {"docx"}:
        df = from_docx(file.file)
    elif extension in {"odt"}:
        df = from_odt(file.file)
    elif extension in {"pdf"}:
        df = from_pdf(file.file)
    elif extension in {"doc"}:
        return "ERROR: Not yet supported"

    return FUNCTIONS.get(format, lambda x: 404)(df)
