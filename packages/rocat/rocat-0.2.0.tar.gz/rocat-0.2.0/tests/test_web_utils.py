# tests/test_web_utils.py
import os
import pytest
from rocat.web_utils import get_web, get_youtube, get_search
from rocat.file_utils import get_whisper

def test_get_web():
    url = "https://www.naver.com"
    text = get_web(url)
    html = get_web(url, type="html")
    
    assert isinstance(text, str)
    assert len(text) > 0
    
    assert html.find("h1") is not None
    
    with pytest.raises(ValueError):
        get_web(url, type="invalid")

def test_get_youtube():
    url = "https://www.youtube.com/watch?v=mQG7vN8UYLU"
    transcript = get_youtube(url)
    
    assert isinstance(transcript, str)
    assert len(transcript) > 0

def test_get_whisper():
    audio_file = "tests/test.mp3"
    transcription = get_whisper(audio_file)
    
    assert isinstance(transcription, str)
    assert len(transcription) > 0

def test_get_search():
    query = "Python programming language"
    results = get_search(query)
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "link" in results[0]
    assert "snippet" in results[0]
