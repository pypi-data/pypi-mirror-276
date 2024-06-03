# rocat/language_model.py
from openai import OpenAI
from rocat.config import get_api_key
import requests
import json
import uuid
import anthropic
from .config import get_api_key
from .language_utils import _convert_language_code

MODEL_MAP = {
    "gpt3": "gpt-3.5-turbo",
    "gpt4o": "gpt-4o",
    "opus": "claude-3-opus-20240229",
    "haiku": "claude-3-haiku-20240307",
    "sonnet": "claude-3-sonnet-20240229",
    "clova": "HCX-003"
}

def run_model(model, prompt, system_prompt="", temperature=0.7, top_p=1, max_tokens=1024, output="default", lang="", tools=[], stream=False):
    """
    주어진 모델을 사용하여 프롬프트에 대한 응답을 생성합니다.
    
    Parameters:
        model (str): 사용할 모델의 이름.
        prompt (str): 모델에 입력할 프롬프트.
        system_prompt (str): 시스템 프롬프트, 대화의 맥락을 설정하는 데 사용됩니다 (옵션).
        temperature (float): 생성의 무작위성을 결정하는 값.
        top_p (float): 토큰 확률의 누적 분포 임곗값.
        max_tokens (int): 생성할 최대 토큰 수.
        output (str): 응답의 출력 형식 (default, word, sentence, bullet, json).
        lang (str): 응답 언어 코드 (ISO 639-1).
        tools (list): 사용할 도구 목록.
        stream (bool): 스트림 모드 사용 여부 (기본값: False).
    
    Returns:
        str: 생성된 텍스트 응답 (stream=False인 경우).
        generator: 텍스트를 스트리밍하는 제너레이터 (stream=True인 경우).
    """
    full_model_name = MODEL_MAP.get(model.lower())
    if not full_model_name:
        raise ValueError(f"Unknown model: {model}")
    
    if "gpt" in model.lower():
        return _run_openai(full_model_name, prompt, system_prompt, temperature, top_p, max_tokens, stream)
    elif "claude" in full_model_name or "opus" in full_model_name or "haiku" in full_model_name or "sonnet" in full_model_name:
        return _run_anthropic(full_model_name, prompt, system_prompt, temperature, top_p, max_tokens, output, lang, tools, stream)
    elif "clova" in model.lower():
        return _run_clova(full_model_name, prompt, temperature, top_p, max_tokens)
    else:
        raise ValueError(f"Unknown model: {model}")

def _run_openai(model, prompt, system_prompt="", temperature=0.7, top_p=1, max_tokens=1024, stream=False):
    key = get_api_key("openai")
    client = OpenAI(api_key=key)
    
    messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
    
    if isinstance(prompt, str):
        prompt = [prompt]
    
    for p in prompt:
        messages.append({"role": "user", "content": p})
    
    if stream:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content




def _run_anthropic(model_name, prompt, system_prompt="", temperature=0.7, top_p=1, max_tokens=1024, output="default", lang="", tools=[], stream=False):
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
        if stream:
            with anth_client.messages.stream(
                model=model_name,
                max_tokens=max_tokens,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
            ) as stream:
                for text in stream.text_stream:
                    yield text
        else:
            response = anth_client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                messages=messages,
                temperature=temperature,
                top_p=top_p
            )
            content = response.content
            return "\n".join([block.text for block in content if hasattr(block, 'text')])



def _run_clova(model, prompt, temperature=0.7, top_p=0.8, max_tokens=256):
    host = 'https://clovastudio.stream.ntruss.com'
    
    api_key = get_api_key("naver_clovastudio")
    api_key_primary_val = get_api_key("naver_apigw")
    
    request_id = str(uuid.uuid4())

    headers = {
        'X-NCP-CLOVASTUDIO-API-KEY': api_key,
        'X-NCP-APIGW-API-KEY': api_key_primary_val,
        'X-NCP-CLOVASTUDIO-REQUEST-ID': request_id,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'text/event-stream'
    }

    request_data = {
        'messages': [{"role": "user", "content": prompt}],
        'topP': top_p,
        'topK': 0,
        'maxTokens': max_tokens,
        'temperature': temperature,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }

    with requests.post(host + f'/testapp/v1/chat-completions/{model}',
                       headers=headers, json=request_data, stream=True) as r:
        content = ""
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                if "data:" in decoded_line:
                    _, data = decoded_line.split("data:")
                    data = data.strip()
                    if data != "[DONE]":
                        event_data = json.loads(data)
                        if "message" in event_data:
                            content += event_data["message"]["content"]
        
        return content.strip()
