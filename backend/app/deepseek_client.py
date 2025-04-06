import os
import json
import requests
from typing import List, Dict, Any, Generator
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DeepseekClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Deepseek API key not found in environment variables")
        
        self.base_url = "https://api.deepseek.com"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def chat_completion(self, messages: List[Dict[str, str]], stream: bool = False) -> Any:
        """
        发送聊天请求到 Deepseek API
        
        Args:
            messages: 消息列表，每个消息包含 role 和 content
            stream: 是否使用流式响应
            
        Returns:
            如果 stream=False，返回完整的响应对象
            如果 stream=True，返回流式响应
        """
        url = f"{self.base_url}/v1/chat/completions"
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "stream": stream
        }
        
        if not stream:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        else:
            return requests.post(url, headers=self.headers, json=payload, stream=True)
    
    def generate_stream_response(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """
        生成流式响应的生成器
        
        Args:
            messages: 消息列表
            
        Returns:
            生成器，每次产生消息的增量部分
        """
        response = self.chat_completion(messages, stream=True)
        
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                if line_text.startswith('data: '):
                    if line_text == 'data: [DONE]':
                        break
                    
                    json_str = line_text[6:]  # 去除 "data: " 前缀
                    try:
                        chunk = json.loads(json_str)
                        if chunk.get('choices') and chunk['choices'][0].get('delta') and chunk['choices'][0]['delta'].get('content'):
                            content = chunk['choices'][0]['delta']['content']
                            yield content
                    except json.JSONDecodeError:
                        continue 