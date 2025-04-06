import requests
import json
import time

BASE_URL = "http://localhost:3004"

def test_health_check():
    """测试健康检查端点"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print("="*50)
        print("健康检查")
        print("="*50)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print("="*50)
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

def test_chat_endpoint():
    """测试聊天端点"""
    try:
        data = {
            "messages": [
                {"role": "system", "content": "你是一个有用的助手"},
                {"role": "user", "content": "你好，请简短介绍一下你自己"}
            ],
            "session_id": f"test-session-{int(time.time())}",
            "stream": False
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat", 
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print("="*50)
        print("聊天测试")
        print("="*50)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print("="*50)
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

def test_history_endpoint():
    """测试历史记录端点"""
    try:
        session_id = f"test-session-{int(time.time())}"
        
        # 先发送一条消息创建历史记录
        chat_data = {
            "messages": [
                {"role": "system", "content": "你是一个有用的助手"},
                {"role": "user", "content": "你好"}
            ],
            "session_id": session_id,
            "stream": False
        }
        
        requests.post(
            f"{BASE_URL}/api/chat", 
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        # 然后获取历史记录
        history_data = {
            "session_id": session_id
        }
        
        response = requests.post(
            f"{BASE_URL}/api/history", 
            json=history_data,
            headers={"Content-Type": "application/json"}
        )
        
        print("="*50)
        print("历史记录测试")
        print("="*50)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print("="*50)
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始测试 API...")
    
    success = True
    
    # 测试健康检查
    if not test_health_check():
        print("健康检查测试失败")
        success = False
    
    # 测试聊天端点
    if not test_chat_endpoint():
        print("聊天测试失败")
        success = False
    
    # 测试历史记录端点
    if not test_history_endpoint():
        print("历史记录测试失败")
        success = False
    
    if success:
        print("所有测试通过！API 服务正常工作。")
    else:
        print("一些测试失败，请检查以上错误信息。") 