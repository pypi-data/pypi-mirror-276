# tests/test_audio_utils.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
from rocat.audio_utils import get_whisper

@patch('builtins.open', new_callable=mock_open, read_data=b"fake audio data")
@patch('rocat.audio_utils.get_api_key', return_value="fake_api_key")
@patch('rocat.audio_utils.OpenAI')
def test_get_whisper(mock_openai, mock_get_api_key, mock_open):
    mock_client = MagicMock()
    mock_transcription = MagicMock()
    mock_transcription.create.return_value = "This is a transcribed text."
    mock_client.audio.transcriptions = mock_transcription
    mock_openai.return_value = mock_client

    result = get_whisper("fake_audio_file.wav")

    mock_open.assert_called_once_with("fake_audio_file.wav", "rb")
    mock_get_api_key.assert_called_once_with("openai")
    mock_openai.assert_called_once_with(api_key="fake_api_key")
    assert result == "This is a transcribed text."