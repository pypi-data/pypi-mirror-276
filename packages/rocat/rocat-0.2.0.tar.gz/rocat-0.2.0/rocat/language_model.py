# rocat/language_model.py
from openai import OpenAI
import anthropic
from .config import get_api_key
from .language_utils import _convert_language_code

def run_gpt(prompt, system_prompt="", temperature=0.7, top_p=1, max_tokens=1024, key=None):
    """
    OpenAI GPT-3.5 모델을 사용하여 주어진 프롬프트에 대한 응답을 생성합니다.
    
    Parameters:
        prompt (str): 모델에 입력할 프롬프트.
        system_prompt (str): 시스템 프롬프트, 대화의 맥락을 설정하는 데 사용됩니다 (옵션).
        temperature (float): 생성의 무작위성을 결정하는 값.
        top_p (float): 토큰 확률의 누적 분포 임곗값.
        max_tokens (int): 생성할 최대 토큰 수.
    
    Returns:
        str: 생성된 텍스트 응답.
    """
    key = get_api_key("openai")
    client = OpenAI(api_key=key)
    
    messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
    
    if isinstance(prompt, str):
        prompt = [prompt]
    
    for p in prompt:
        messages.append({"role": "user", "content": p})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

def run_gpt4( prompt, system_prompt="", key=None, temperature=0.7, top_p=1, max_tokens=1024):
    """
    OpenAI GPT-4 모델을 사용하여 주어진 프롬프트에 대한 응답을 생성합니다.
    
    Parameters:
        prompt (str): 모델에 입력할 프롬프트.
        system_prompt (str): 시스템 프롬프트, 대화의 맥락을 설정하는 데 사용됩니다 (옵션).
        temperature (float): 생성의 무작위성을 결정하는 값.
        top_p (float): 토큰 확률의 누적 분포 임곗값.
        max_tokens (int): 생성할 최대 토큰 수.
    
    Returns:
        str: 생성된 텍스트 응답.
    """
    key = get_api_key("openai")
    client = OpenAI(api_key=key)
    
    messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
    
    if isinstance(prompt, str):
        prompt = [prompt]
    
    for p in prompt:
        messages.append({"role": "user", "content": p})
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

def run_claude(prompt, model_name="claude-3-sonnet-20240229", system_prompt="", temperature=0.7, top_p=1, max_tokens=1024, output="default", lang="", tools=[]):
    """
    Anthropic의 Claude 모델을 사용하여 주어진 프롬프트에 대한 응답을 생성하고 특정 형식으로 출력합니다.

    Parameters:
        prompt (str or list of str): 모델에 입력할 프롬프트.
        model_name (str): 사용할 Claude 모델의 이름.
        system_prompt (str): 대화 컨텍스트를 위한 시스템 프롬프트 (옵션).
        temperature (float): 생성의 무작위성을 결정하는 값.
        top_p (float): 토큰 확률의 누적 분포 임곗값.
        max_tokens (int): 생성할 최대 토큰 수.
        output (str): 응답의 출력 형식 (default, word, sentence, bullet, json).
        lang (str): 응답 언어 코드 (ISO 639-1).
        tools (list): 사용할 도구 목록.

    Returns:
        str: 생성된 텍스트 응답. 여러 개의 텍스트 블록이 있을 경우 이를 연결하여 반환합니다.
    """
    key = get_api_key("anthropic")
    anth_client = anthropic.Anthropic(api_key=key)
    output_format = {
        "default": "",
        "word": " Don't explain, keep your output to very short one word.",
        "sentence": " Keep your output to very short one sentence.",
        "bullet": " Don't explain, keep your output in bullet points. Don't say anything else.",
        "json": " Don't explain, keep your output in json format. Don't say anything else."
    }
    lang_output = ""
    if lang:
        language = _convert_language_code(lang)
        if language is not None:
            lang_output = f" Please Write in {language} without any additional explanations."

    system_prompt += output_format.get(output, "") + lang_output

    messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
    
    if isinstance(prompt, str):
        prompt = [prompt]
    for user_message in prompt:
        messages.append({"role": "user", "content": user_message})

    if not tools:
        response = anth_client.messages.create(
            model=model_name,
            max_tokens=max_tokens,
            messages=messages,
            temperature=temperature,
            top_p=top_p
        )
        content = response.content
        return "\n".join([block.text for block in content if hasattr(block, 'text')])
    else:
        # Tool 처리 로직 추가
        tool_format = [{
            "name": tool[0],
            "description": tool[1],
            "input_schema": {
                "type": "object",
                "properties": {key: {"type": "string", "description": value} for key, value in tool[2].items()}
            }
        } for tool in tools]

        response = anth_client.beta.tools.messages.create(
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            tools=tool_format,
            system=system_prompt,
            messages=messages
        )
        # 도구 사용 결과 처리 로직 추가
        content = response.content
        return "\n".join([block.text for block in content if hasattr(block, 'text')])


def run_opus(prompt, system_prompt="", temperature=0.7, top_p=1, max_tokens=1024):
    """
    Anthropic의 Claude-3-Opus 모델을 사용하여 주어진 프롬프트에 대한 응답을 생성합니다.
    이 함수는 run_claude 함수의 특정 모델을 사용하는 버전입니다.
    
    Parameters와 Returns는 run_claude 함수와 동일합니다.
    """
    return run_claude(prompt, model_name="claude-3-opus-20240229", system_prompt=system_prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)

def run_haiku(prompt, system_prompt="", temperature=0.7, top_p=1, max_tokens=1024):
    """
    Anthropic의 Claude-3-Haiku 모델을 사용하여 주어진 프롬프트에 대한 응답을 생성합니다.
    이 함수는 run_claude 함수의 특정 모델을 사용하는 버전입니다.
    
    Parameters와 Returns는 run_claude 함수와 동일합니다.
    """
    return run_claude(prompt, model_name="claude-3-haiku-20240307", system_prompt=system_prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)

def run_sonnet(prompt, system_prompt="", temperature=0.7, top_p=1, max_tokens=1024):
    """
    Anthropic의 Claude-3-Sonnet 모델을 사용하여 주어진 프롬프트에 대한 응답을 생성합니다.
    이 함수는 run_claude 함수의 특정 모델을 사용하는 버전입니다.
    
    Parameters와 Returns는 run_claude 함수와 동일합니다.
    """
    return run_claude(prompt, model_name="claude-3-sonnet-20240229", system_prompt=system_prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)