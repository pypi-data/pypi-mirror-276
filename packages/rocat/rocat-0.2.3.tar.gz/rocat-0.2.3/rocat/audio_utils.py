# rocat/audio_utils.py
from rocat.config import get_api_key
from openai import OpenAI

def get_whisper(audio_file):
    """
    오디오 파일을 Whisper API를 사용하여 텍스트로 변환합니다.
    
    Args:
        audio_file (str): 오디오 파일 경로.
    
    Returns:
        str: 변환된 텍스트.
    """
    api_key = get_api_key("openai")
    client = OpenAI(api_key=api_key)
    with open(audio_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            response_format="text"
        )
    return transcription