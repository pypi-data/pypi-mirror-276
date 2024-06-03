# tests/test_language_model.py
import pytest
from rocat.language_model import run_model
from unittest.mock import patch, MagicMock

@pytest.mark.parametrize("model, prompt, expected_response, stream", [
    ("gpt3", "Tell me a joke", "This is a joke.", False),
    ("gpt4o", "What is the capital of France?", "The capital of France is Paris.", False),
    ("opus", "Write a short poem about the moon", "This is a short poem about the moon.", False),
    ("haiku", "Write a haiku about the ocean", "This is a haiku about the ocean.", False),
    ("sonnet", "Write a sonnet about love", "This is a sonnet about love.", False),
    ("clova", "Summarize the benefits of exercise in one sentence", "Exercise improves health.", False),
    ("gpt3", "Tell me a story", "Once upon a time...", True),
    ("opus", "Describe a beautiful landscape", "The sun rises over the mountains...", True)
])
@patch('rocat.language_model._run_openai')
@patch('rocat.language_model._run_anthropic')
@patch('rocat.language_model._run_clova')
def test_run_model(mock_run_clova, mock_run_anthropic, mock_run_openai, model, prompt, expected_response, stream):
    if "gpt" in model:
        if stream:
            mock_run_openai.return_value = (chunk for chunk in expected_response)
        else:
            mock_run_openai.return_value = expected_response
    elif "claude" in model or "opus" in model or "haiku" in model or "sonnet" in model:
        if stream:
            mock_run_anthropic.return_value = (chunk for chunk in expected_response)
        else:
            mock_run_anthropic.return_value = expected_response
    elif "clova" in model:
        mock_run_clova.return_value = expected_response

    response = run_model(model, prompt, stream=stream)

    if stream:
        response_text = "".join(response)
        assert response_text == expected_response
    else:
        assert response == expected_response

if __name__ == "__main__":
    pytest.main()