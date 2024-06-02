#tests/test_image_utils.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
from rocat.image_utils import extract_text_from_image
import base64

@patch('builtins.open', new_callable=mock_open, read_data=b"fake image data")
@patch('rocat.image_utils.get_api_key', return_value="fake_api_key")
@patch('rocat.image_utils.OpenAI')
def test_extract_text_from_image(mock_openai, mock_get_api_key, mock_file):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "This is extracted text."
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client

    result = extract_text_from_image("fake_image_file.jpg")

    mock_file.assert_any_call("fake_image_file.jpg", "rb")
    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "주어진 이미지에서 kr 언어를 텍스트로 추출합니다"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64.b64encode(b'fake image data').decode('utf-8')}",
                            "detail": "auto"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    assert result == "This is extracted text."

if __name__ == "__main__":
    pytest.main()
