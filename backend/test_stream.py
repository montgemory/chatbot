import requests
import json
import time

BASE_URL = "http://localhost:3004"

def test_stream_response():
    """测试流式响应端点"""
    try:
        data = {
            "messages": [
                {"role": "system", "content": "你是一个有用的助手"},
                {"role": "user", "content": "请用5个词语描述深圳"}
            ],
            "session_id": f"test-stream-{int(time.time())}"
        }
        
        # 流式请求需要使用 .iter_lines() 来读取响应
        response = requests.post(
            f"{BASE_URL}/api/chat/stream", 
            json=data,
            headers={"Content-Type": "application/json"},
            stream=True
        )
        
        print("="*50)
        print("流式响应测试")
        print("="*50)
        
        if response.status_code != 200:
            print(f"错误状态码: {response.status_code}")
            return False
        
        # 处理 SSE 格式的响应
        full_response = ""
        print("收到的响应流:")
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                # 解析 SSE 格式
                if line_text.startswith('data:'):
                    data_part = line_text[5:].strip()  # 去除 "data:" 前缀并清除空格
                    if data_part:
                        print(data_part, end="", flush=True)
                        full_response += data_part
                elif 'event: done' in line_text:
                    print("\n流式响应完成")
                    break
                elif 'event: error' in line_text:
                    print(f"\n错误: {line_text}")
                    return False
        
        print("\n" + "="*50)
        print(f"完整响应: {full_response}")
        print("="*50)
        return True
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始测试流式响应...")
    
    if test_stream_response():
        print("流式响应测试通过！")
    else:
        print("流式响应测试失败，请检查上面的错误信息。") 