from rocat.config import get_api_key
from openai import OpenAI
import base64

def extract_text_from_image(image_path, language='kr', detail='auto'):
    """
    이미지에서 텍스트를 추출합니다 (OCR).

    Args:
        image_path (str): 이미지 파일 경로.
        language (str): 추출할 텍스트의 언어. 기본값은 'kr'(한국어)입니다.
        detail (str): 이미지 처리 상세 수준. 'low', 'high', 또는 'auto'. 기본값은 'auto'입니다.

    Returns:
        str: 추출된 텍스트.
    """
    api_key = get_api_key("openai")
    openai = OpenAI(api_key)

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": f"주어진 이미지에서 {language} 언어를 텍스트로 추출합니다"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}",
                            "detail": detail
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    extracted_text = response.choices[0].message.content.strip()
    return extracted_text
