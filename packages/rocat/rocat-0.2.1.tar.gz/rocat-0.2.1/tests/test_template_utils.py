# tests/test_template_utils.py
import pytest
from rocat.template_utils import prompt_template

def test_prompt_template():
    instruction = "Summarize the given text"
    constraints = "Max 50 words, Focus on key points"
    output_format = "Bullet points"
    input_text = "Sample text for testing"
    
    prompt = prompt_template(instruction, constraints, output_format, input_text)
    assert isinstance(prompt, str)
    assert instruction in prompt
    assert constraints.replace(",", "\n") in prompt
    assert output_format in prompt
    assert input_text in prompt

if __name__ == "__main__":
    pytest.main()
