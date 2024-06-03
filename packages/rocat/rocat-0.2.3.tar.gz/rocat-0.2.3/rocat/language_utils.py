# rocat/language_utils.py
import pycountry

def _convert_language_code(iso_639_1_code):
    """
    ISO 639-1 언어 코드를 해당 언어의 전체 이름으로 변환합니다.

    :param iso_639_1_code: 변환할 ISO 639-1 언어 코드 (예: "en", "ko", "zh-tw", "zh-cn")
    :return: 언어 코드에 해당하는 언어의 전체 이름 (소문자), 또는 언어 코드가 유효하지 않은 경우 None
    """
    try:
        language = pycountry.languages.get(alpha_2=iso_639_1_code)

        if iso_639_1_code.lower() == "zh-tw":
            return "traditional chinese(taiwan)"
        elif iso_639_1_code.lower() == "zh-cn":
            return "simplified chinese"

        if language:
            return language.name.lower()
        else:
            return None
    except:
        return None