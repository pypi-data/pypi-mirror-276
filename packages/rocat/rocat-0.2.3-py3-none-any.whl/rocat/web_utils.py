# rocat/web_utils.py
from .config import get_api_key
from serpapi import GoogleSearch
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

def get_web(url, type="text"):
    """ 
    주어진 URL에서 웹 페이지를 가져옵니다.
    
    Args:
        url (str): 웹 페이지의 URL.
        type (str): 반환할 데이터의 형식. "text" 또는 "html". 기본값은 "text".
    
    Returns:
        str or BeautifulSoup: 웹 페이지의 텍스트 또는 HTML 파싱 결과.
    
    Raises:
        ValueError: 지원되지 않는 type 값인 경우 발생.
    """
    response = requests.get(url)
    if type == "text":
        return response.text
    elif type == "html":
        return BeautifulSoup(response.text, "html.parser")
    else:
        raise ValueError(f"Unsupported type: {type}")
    
def get_youtube(url):
    """ 
    YouTube URL에서 동영상 자막을 가져옵니다.
    
    Args:
        url (str): YouTube 동영상 URL.
    
    Returns:
        str: 동영상 자막 텍스트.
    """
    video_id = url.split("watch?v=")[1]
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
    transcript = " ".join([t['text'] for t in transcript_list])
    return transcript


def get_search(query):
    """ 
    SerpAPI를 사용하여 검색 쿼리에 대한 검색 결과를 가져옵니다.
    
    Args:
        query (str): 검색 쿼리.
    
    Returns:
        list: 검색 결과 리스트. 각 결과는 딕셔너리 형태로 제목, 링크, 스니펫을 포함합니다.
    """
    api_key = get_api_key("serpapi")
    params = {
        "q": query,
        "api_key": api_key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    search_results = []
    for result in results.get("organic_results", []):
        search_result = {
            "title": result.get("title", ""),
            "link": result.get("link", ""),
            "snippet": result.get("snippet", "")
        }
        search_results.append(search_result)

    return search_results
