import os
import sys
from dotenv import load_dotenv

# 添加当前目录到 sys.path，以便导入应用模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
load_dotenv()

from app.deepseek_client import DeepseekClient

def test_text_completion():
    """测试基本的文本完成功能"""
    client = DeepseekClient()
    
    # 创建测试消息
    messages = [
        {"role": "system", "content": "你是一个有用的助手，请用中文回答问题。"},
        {"role": "user", "content": "你好，请介绍一下你自己。"}
    ]
    
    # 发送请求
    response = client.chat_completion(messages)
    
    # 打印响应
    print("="*50)
    print("文本完成测试")
    print("="*50)
    print(f"响应：\n{response['choices'][0]['message']['content']}")
    print("="*50)
    return response

def test_stream_completion():
    """测试流式文本完成功能"""
    client = DeepseekClient()
    
    # 创建测试消息
    messages = [
        {"role": "system", "content": "你是一个有用的助手，请用中文回答问题。"},
        {"role": "user", "content": "你好，请用三句话介绍一下深圳这个城市。"}
    ]
    
    print("="*50)
    print("流式完成测试")
    print("="*50)
    
    # 获取流式响应
    response_stream = client.generate_stream_response(messages)
    
    # 打印每个响应块
    full_response = ""
    print("响应：")
    for content in response_stream:
        full_response += content
        print(content, end="", flush=True)
    
    print("\n" + "="*50)
    
    return full_response

if __name__ == "__main__":
    print("开始测试 Deepseek API...")
    
    # 测试文本完成
    test_text_completion()
    
    print("\n")
    
    # 测试流式完成
    test_stream_completion()
    
    print("\n测试完成！") 