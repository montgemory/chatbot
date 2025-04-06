import { Message } from '../types';

// 使用环境变量或默认API URL
declare global {
  interface Window {
    env: {
      NEXT_PUBLIC_API_URL: string;
    };
  }
}

const API_URL = typeof window !== 'undefined' 
  ? (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3004')
  : 'http://localhost:3004';

export async function fetchChatHistory(sessionId: string): Promise<Message[]> {
  try {
    const response = await fetch(`${API_URL}/api/history`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ session_id: sessionId }),
    });
    
    if (!response.ok) {
      throw new Error('加载聊天历史失败');
    }
    
    const data = await response.json();
    return data.messages || [];
  } catch (error) {
    console.error('获取聊天历史错误:', error);
    throw error;
  }
}

export function sendChatMessageWithSSE(
  messages: Message[], 
  sessionId: string, 
  onMessage: (content: string) => void,
  onError: (error: Error) => void,
  onComplete: () => void
): () => void {
  // 准备请求数据
  const body = JSON.stringify({
    messages,
    session_id: sessionId,
    stream: true
  });
  
  // 编码请求参数为URL查询字符串
  const params = new URLSearchParams({
    data: body
  }).toString();
  
  // 创建EventSource连接
  const eventSource = new EventSource(`${API_URL}/api/chat/stream/sse?${params}`);
  
  let fullResponse = '';
  
  // 消息事件处理
  eventSource.addEventListener('message', (event) => {
    try {
      console.log('收到SSE消息:', event.data);
      
      if (event.data === '[DONE]') {
        console.log('接收到结束标记');
        eventSource.close();
        onComplete();
        return;
      }
      
      // 累积响应
      fullResponse += event.data;
      
      // 回调新内容
      onMessage(fullResponse);
    } catch (error) {
      console.error('处理SSE消息错误:', error);
      onError(new Error('处理消息出错'));
    }
  });
  
  // 错误处理
  eventSource.addEventListener('error', (event) => {
    console.error('SSE错误:', event);
    eventSource.close();
    onError(new Error('流式消息传输错误'));
  });
  
  // 完成事件处理
  eventSource.addEventListener('done', () => {
    console.log('SSE传输完成');
    eventSource.close();
    onComplete();
  });
  
  // 返回取消函数
  return () => {
    console.log('取消SSE连接');
    eventSource.close();
  };
}

// 保留原始fetch方法用于非SSE请求
export async function sendChatMessage(messages: Message[], sessionId: string): Promise<Response> {
  try {
    const response = await fetch(`${API_URL}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages,
        session_id: sessionId,
        stream: true
      }),
    });
    
    if (!response.ok) {
      console.error('发送消息失败:', response.status, response.statusText);
      throw new Error(`发送消息失败: ${response.status} ${response.statusText}`);
    }
    
    return response;
  } catch (error) {
    console.error('发送消息错误:', error);
    throw error;
  }
}

export async function healthCheck(): Promise<{ status: string; version: string }> {
  try {
    const response = await fetch(`${API_URL}/api/health`);
    
    if (!response.ok) {
      throw new Error('健康检查失败');
    }
    
    return await response.json();
  } catch (error) {
    console.error('健康检查错误:', error);
    throw error;
  }
}