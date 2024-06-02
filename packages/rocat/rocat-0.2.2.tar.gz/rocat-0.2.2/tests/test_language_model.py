#tests/test_language_model.py   

import pytest
from rocat.language_model import run_model
from unittest.mock import patch, MagicMock

@pytest.mark.parametrize("model, prompt, expected_response", [
    ("gpt3", "Tell me a joke", "This is a joke."),
    ("gpt4o", "What is the capital of France?", "The capital of France is Paris."),
    ("opus", "Write a short poem about the moon", "This is a short poem about the moon."),
    ("haiku", "Write a haiku about the ocean", "This is a haiku about the ocean."),
    ("sonnet", "Write a sonnet about love", "This is a sonnet about love."),
    ("clova", "Summarize the benefits of exercise in one sentence", "Exercise improves health.")
])
@patch('rocat.language_model._run_openai')
@patch('rocat.language_model._run_anthropic')
@patch('rocat.language_model._run_clova')
def test_run_model(mock_run_clova, mock_run_anthropic, mock_run_openai, model, prompt, expected_response):
    if "gpt" in model:
        mock_run_openai.return_value = expected_response
    elif "claude" in model or "opus" in model or "haiku" in model or "sonnet" in model:
        mock_run_anthropic.return_value = expected_response
    elif "clova" in model:
        mock_run_clova.return_value = expected_response

    response = run_model(model, prompt)
    assert response == expected_response

if __name__ == "__main__":
    pytest.main()
