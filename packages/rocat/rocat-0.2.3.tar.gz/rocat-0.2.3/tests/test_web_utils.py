# tests/test_web_utils.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
from rocat.web_utils import get_web, get_youtube, get_search
from rocat.audio_utils import get_whisper

def test_get_web():
    url = "https://www.naver.com"
    text = get_web(url)
    html = get_web(url, type="html")
    
    assert isinstance(text, str)
    assert len(text) > 0
    
    assert html.find("h1") is not None
    
    with pytest.raises(ValueError):
        get_web(url, type="invalid")

@patch('rocat.web_utils.YouTubeTranscriptApi.get_transcript')
def test_get_youtube(mock_get_transcript):
    mock_get_transcript.return_value = [{'text': 'This is a test transcript.'}]
    url = "https://www.youtube.com/watch?v=mQG7vN8UYLU"
    transcript = get_youtube(url)
    
    assert isinstance(transcript, str)
    assert "This is a test transcript." in transcript
    mock_get_transcript.assert_called_once()


@patch('rocat.web_utils.GoogleSearch.get_dict')
def test_get_search(mock_get_dict):
    mock_get_dict.return_value = {
        "organic_results": [
            {"title": "Python programming", "link": "http://example.com", "snippet": "Python is a programming language."}
        ]
    }
    query = "Python programming language"
    results = get_search(query)
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "link" in results[0]
    assert "snippet" in results[0]

if __name__ == "__main__":
    pytest.main()
