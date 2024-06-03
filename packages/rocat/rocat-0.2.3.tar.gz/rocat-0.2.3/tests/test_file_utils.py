#tests/test_file_utils.py
from io import BytesIO
from pypdf import PdfReader
import io
import pytest
from unittest.mock import MagicMock, mock_open, patch
from rocat.file_utils import (
    get_txt, get_xls, get_xlsx, excel_get_field, get_doc, get_docx, get_ppt, get_pptx, 
    get_csv, get_pdf, get_hwp, get_hwpx
)

@patch("builtins.open", new_callable=mock_open, read_data="This is a test file.")
def test_get_txt(mock_file):
    result = get_txt("test.txt")
    assert result == "This is a test file."
    mock_file.assert_called_once_with("test.txt", "r", encoding="utf-8")

@patch('rocat.file_utils.xlrd.open_workbook')
def test_get_xls(mock_open_workbook):
    # Mocking xlrd.open_workbook
    mock_workbook = MagicMock()
    mock_sheet = MagicMock()
    mock_sheet.ncols = 2
    mock_sheet.col_values.side_effect = [
        ["Header 1", "Value 1"],
        ["Header 2", "Value 2"]
    ]
    mock_workbook.sheet_by_index.return_value = mock_sheet
    mock_open_workbook.return_value = mock_workbook

    result = get_xls("test.xls")
    expected_data = {"A": ["Header 1", "Value 1"], "B": ["Header 2", "Value 2"]}
    assert result == expected_data

@patch('rocat.file_utils.load_workbook')
def test_get_xlsx(mock_load_workbook):
    # Mocking openpyxl.load_workbook
    mock_workbook = MagicMock()
    mock_sheet = MagicMock()
    mock_sheet.iter_cols.return_value = [
        ("Header 1", "Value 1"),
        ("Header 2", "Value 2")
    ]
    mock_workbook.__getitem__.return_value = mock_sheet
    mock_load_workbook.return_value = mock_workbook

    result = get_xlsx("test.xlsx", sheet="Sheet1")
    expected_data = {"A": ["Header 1", "Value 1"], "B": ["Header 2", "Value 2"]}
    assert result == expected_data

@pytest.mark.parametrize("field_number, excel_data, expected_result", [
    ("A1", {"A": ["Header 1", "Value 1", "Value 3"], "B": ["Header 2", "Value 2", "Value 4"]}, "Header 1"),
    ("B2", {"A": ["Header 1", "Value 1", "Value 3"], "B": ["Header 2", "Value 2", "Value 4"]}, "Value 2"),
    (["A1", "B2"], {"A": ["Header 1", "Value 1", "Value 3"], "B": ["Header 2", "Value 2", "Value 4"]}, ["Header 1", "Value 2"]),
    ("A2:B3", {"A": ["Header 1", "Value 1", "Value 3"], "B": ["Header 2", "Value 2", "Value 4"]}, ["Value 1", "Value 2", "Value 3", "Value 4"])
])
def test_excel_get_field(field_number, excel_data, expected_result):
    result = excel_get_field(field_number, excel_data)
    assert result == expected_result

@patch('rocat.file_utils.extract_doc_text', return_value="This is a test DOC document.")
@patch('rocat.file_utils.olefile.OleFileIO')
def test_get_doc(mock_ole, mock_extract_doc_text):
    mock_ole_instance = mock_ole.return_value
    mock_ole_instance.exists.return_value = True
    mock_ole_instance.openstream.return_value = MagicMock()
    mock_ole_instance.listdir.return_value = [["\x05HwpSummaryInformation"], ["WordDocument"]]

    result = get_doc("test.doc")
    assert result == "This is a test DOC document."
    
@patch('docx2txt.process', return_value="This is a test DOCX document.")
def test_get_docx(mock_process):
    result = get_docx("test.docx")
    assert result == "This is a test DOCX document."
    mock_process.assert_called_once_with("test.docx")

def test_get_ppt():
    pass

@patch('pptx.Presentation')
def test_get_pptx(mock_presentation):
    mock_slide = MagicMock()
    mock_shape = MagicMock()
    mock_shape.text = "This is a test PPTX document."
    mock_slide.shapes = [mock_shape]
    mock_presentation.return_value.slides = [mock_slide]

    result = get_pptx("test.pptx")
    assert result.strip() == "This is a test PPTX document."

@patch("builtins.open", new_callable=mock_open, read_data="Header 1,Header 2\nValue 1,Value 2\nValue 3,Value 4")
def test_get_csv(mock_file):
    result = get_csv("test.csv")
    expected_data = [["Header 1", "Header 2"], ["Value 1", "Value 2"], ["Value 3", "Value 4"]]
    assert result == expected_data
    mock_file.assert_called_once_with("test.csv", "r", encoding="utf-8")


def test_get_pdf():
    pdf_path = "tests/test_pdf.pdf"
    result = get_pdf(pdf_path)
    assert result is not None
    assert "This is a test PDF document." in result.strip()

@patch('rocat.file_utils.read_hwp', return_value="This is a test HWP document.")
def test_get_hwp(mock_read_hwp):
    result = get_hwp("test.hwp")
    assert result == "This is a test HWP document."
    mock_read_hwp.assert_called_once_with("test.hwp")

@patch('rocat.file_utils.read_hwpx', return_value="This is a test HWPX document.")
def test_get_hwpx(mock_read_hwpx):
    result = get_hwpx("test.hwpx")
    assert result == "This is a test HWPX document."
    mock_read_hwpx.assert_called_once_with("test.hwpx")

if __name__ == "__main__":
    pytest.main()
