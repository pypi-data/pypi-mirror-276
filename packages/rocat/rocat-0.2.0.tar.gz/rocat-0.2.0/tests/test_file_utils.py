# tests/test_file_utils.py
import pytest
from unittest.mock import patch, MagicMock
from rocat.file_utils import get_txt, get_xls, get_xlsx, excel_get_field, get_doc, get_docx, get_ppt, get_pptx, get_csv, get_pdf, get_hwp, get_hwpx

def test_get_txt():
    # get_txt 함수 테스트
    result = get_txt("test.txt")
    assert result == "This is a test file."

def test_get_xls():
    # get_xls 함수 테스트
    result = get_xls("test.xls")
    assert result["A"][0] == "Header 1"
    assert result["B"][1] == "Value 2"

def test_get_xlsx():
    # get_xlsx 함수 테스트
    result = get_xlsx("test.xlsx", sheet="Sheet1")
    assert result["A"][0] == "Header 1"
    assert result["B"][1] == "Value 2"

def test_excel_get_field():
    # excel_get_field 함수 테스트
    excel_data = {
        "A": ["Header 1", "Value 1", "Value 3"],
        "B": ["Header 2", "Value 2", "Value 4"]
    }

    result1 = excel_get_field("A1", excel_data)
    assert result1 == "Header 1"

    result2 = excel_get_field("B2", excel_data)
    assert result2 == "Value 2"

    result3 = excel_get_field(["A1", "B2"], excel_data)
    assert result3 == ["Header 1", "Value 2"]

    result4 = excel_get_field("A2:B3", excel_data)
    assert result4 == ["Value 1", "Value 2", "Value 3", "Value 4"]

@patch('rocat.file_utils.extract_doc_text', return_value="This is a test DOC document.")
def test_get_doc(mock_extract_doc_text):
    # get_doc 함수 테스트
    result = get_doc("test.doc")
    assert result == "This is a test DOC document."
    mock_extract_doc_text.assert_called_once()

@patch('docx2txt.process', return_value="This is a test DOCX document.")
def test_get_docx(mock_process):
    # get_docx 함수 테스트
    result = get_docx("test.docx")
    assert result == "This is a test DOCX document."
    mock_process.assert_called_once_with("test.docx")

def test_get_ppt():
    # 추후 구현할 get_ppt 함수에 대한 테스트
    pass

@patch('pptx.Presentation')
def test_get_pptx(mock_presentation):
    # get_pptx 함수 테스트
    mock_slide = MagicMock()
    mock_shape = MagicMock()
    mock_shape.text = "This is a test PPTX document."
    mock_slide.shapes = [mock_shape]
    mock_presentation.return_value.slides = [mock_slide]

    result = get_pptx("test.pptx")
    assert result.strip() == "This is a test PPTX document."

def test_get_csv():
    # get_csv 함수 테스트
    result = get_csv("test.csv")
    assert result == [["Header 1", "Header 2"], ["Value 1", "Value 2"], ["Value 3", "Value 4"]]

def test_get_pdf():
    # get_pdf 함수 테스트
    result = get_pdf("test.pdf")
    assert "This is a test PDF document." in result

@patch('rocat.file_utils.read_hwp', return_value="This is a test HWP document.")
def test_get_hwp(mock_read_hwp):
    # get_hwp 함수 테스트
    result = get_hwp("test.hwp")
    assert result == "This is a test HWP document."
    mock_read_hwp.assert_called_once_with("test.hwp")

@patch('rocat.file_utils.read_hwpx', return_value="This is a test HWPX document.")
def test_get_hwpx(mock_read_hwpx):
    # get_hwpx 함수 테스트
    result = get_hwpx("test.hwpx")
    assert result == "This is a test HWPX document."
    mock_read_hwpx.assert_called_once_with("test.hwpx")
