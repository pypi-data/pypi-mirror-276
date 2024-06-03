from rocat import language_model

config = None

def set_config(cfg):
    """
    설정을 전역 변수 config에 저장합니다.

    :param cfg: 설정 객체
    """
    global config
    config = cfg

def _run_model(prompt, model):
    """
    선택한 모델을 사용하여 프롬프트를 처리하고 결과를 반환합니다.

    :param prompt: 모델에 입력할 프롬프트 텍스트
    :param model: 사용할 모델의 이름 ("gpt3", "gpt4o", "opus", "haiku", "sonnet", "clova")
    :return: 모델이 생성한 텍스트
    :raises ValueError: 지원하지 않는 모델이 선택된 경우
    """
    return language_model.run_model(model, prompt)

def ai_summarize(text, num_sentences, model="gpt3"):
    """
    주어진 텍스트를 지정된 개수의 문장으로 요약합니다.

    :param text: 요약할 텍스트
    :param num_sentences: 요약본에 포함할 문장의 개수
    :param model: 사용할 모델의 이름 (기본값: "gpt3", 선택 가능한 모델: "gpt3", "gpt4o", "opus", "haiku", "sonnet", "clova")
    :return: 요약된 텍스트
    """
    prompt = f"다음 텍스트를 {num_sentences}개의 문장으로 요약해 주세요:\n\n{text}"
    summary = _run_model(prompt, model)
    return summary

def ai_bullet(text, num, model="gpt3"):
    """
    주어진 텍스트를 지정된 개수의 bullet point로 요약합니다.

    :param text: 요약할 텍스트
    :param num: 생성할 bullet point의 개수
    :param model: 사용할 모델의 이름 (기본값: "gpt3", 선택 가능한 모델: "gpt3", "gpt4o", "opus", "haiku", "sonnet", "clova")
    :return: bullet point로 요약된 텍스트
    """
    prompt = f"다음 텍스트를 {num}개의 bullet point로 요약해 주세요:\n\n{text}"
    bullet_points = _run_model(prompt, model)
    return bullet_points

def ai_translate(text, target_lang, model="gpt3"):
    """
    주어진 텍스트를 지정된 언어로 번역합니다.

    :param text: 번역할 텍스트
    :param target_lang: 번역 대상 언어
    :param model: 사용할 모델의 이름 (기본값: "gpt3", 선택 가능한 모델: "gpt3", "gpt4o", "opus", "haiku", "sonnet", "clova")
    :return: 번역된 텍스트
    """
    prompt = f"다음 텍스트를 {target_lang}로 번역해 주세요:\n\n{text}"
    translation = _run_model(prompt, model)
    return translation
