# rocat/main.py
from rocat.config import load_config
from rocat import web_utils, file_utils, language_model, ai_functions

def initialize():
    """ 
    설정 파일을 로드하고, AI 함수에 설정을 적용합니다.
    
    Raises:
        ValueError: 설정 파일 로드 실패 시 발생.
    """
    config = load_config()
    
    if config is None:
        raise ValueError("Failed to load config file.")
    
    ai_functions.set_config(config)
