# tests/test_ai_funtions.py
import pytest
from rocat.ai_functions import ai_summarize, ai_bullet, ai_translate
from unittest.mock import patch

@pytest.mark.parametrize("model, text, num_sentences", [
    ("gpt3", "Artificial intelligence is a rapidly advancing field.", 1),
    ("gpt4o", "Machine learning is a subset of artificial intelligence.", 2),
    ("opus", "Natural language processing allows computers to understand human language.", 1),
])
@patch('rocat.ai_functions._run_model')
def test_ai_summarize(mock_run_model, model, text, num_sentences):
    mock_run_model.return_value = "This is a summary."
    summary = ai_summarize(text, num_sentences, model)
    assert isinstance(summary, str)
    assert len(summary.strip()) > 0

@pytest.mark.parametrize("model, text, num_bullets", [
    ("gpt3", "Benefits of exercise include improved mood, better health, and increased energy levels.", 3),
    ("gpt4o", "A balanced diet provides the nutrients your body needs to function effectively.", 3),
    ("opus", "Reading books can expand your knowledge, improve your focus, and enhance your empathy.", 3),
])
@patch('rocat.ai_functions._run_model')
def test_ai_bullet(mock_run_model, model, text, num_bullets):
    mock_run_model.return_value = "- Bullet 1\n- Bullet 2\n- Bullet 3"
    bullet_points = ai_bullet(text, num_bullets, model)
    assert isinstance(bullet_points, str)
    assert len(bullet_points.strip()) > 0

@pytest.mark.parametrize("model, text, target_lang", [
    ("gpt3", "Hello, how are you?", "French"),
    ("gpt4o", "Good morning", "Spanish"),
    ("opus", "Thank you", "German"),
])
@patch('rocat.ai_functions._run_model')
def test_ai_translate(mock_run_model, model, text, target_lang):
    mock_run_model.return_value = "Bonjour"
    translation = ai_translate(text, target_lang, model)
    assert isinstance(translation, str)
    assert len(translation.strip()) > 0

if __name__ == "__main__":
    pytest.main()
