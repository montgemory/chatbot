# Deepseek 聊天机器人 API 文档

本文档描述了 Deepseek 聊天机器人后端 API 的使用方法。

## 基本信息

- 基础 URL: `http://localhost:3004` (本地开发)
- 所有请求和响应均使用 JSON 格式
- 所有 API 路径前缀为 `/api`

## 认证

当前版本不需要认证。

## API 端点

### 1. 发送聊天消息 (非流式)

用于发送普通聊天消息并获取回复。

- **URL**: `/api/chat`
- **方法**: `POST`
- **Content-Type**: `application/json`

**请求参数**:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "你是一个有用的助手"
    },
    {
      "role": "user",
      "content": "你好，请介绍一下你自己"
    }
  ],
  "session_id": "可选的会话ID", // 可选，如不提供则自动生成
  "stream": false // 必须设置为 false，否则将返回错误
}
```

**响应**:

```json
{
  "content": "你好！我是一个 AI 助手，我的目标是通过提供信息、回答问题和协助完成各种任务来帮助用户。..."
}
```

**状态码**:

- `200 OK`: 请求成功
- `500 Internal Server Error`: 服务器错误

### 2. 发送流式聊天消息

用于发送聊天消息并获取流式回复。

- **URL**: `/api/chat/stream`
- **方法**: `POST`
- **Content-Type**: `application/json`

**请求参数**:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "你是一个有用的助手"
    },
    {
      "role": "user",
      "content": "你好，请介绍一下你自己"
    }
  ],
  "session_id": "可选的会话ID" // 可选，如不提供则自动生成
}
```

**响应**:

响应使用 SSE (Server-Sent Events) 格式，客户端需要处理以下事件:

- `message`: 包含响应内容的增量
- `done`: 表示流响应结束
- `error`: 发生错误

示例响应流:

```
event: message
data: 你好

event: message
data: ！

event: message
data: 我是

event: message
data: 一个

...

event: done
data: 
```

**状态码**:

- `200 OK`: 请求成功
- `500 Internal Server Error`: 服务器错误

### 3. 获取会话历史记录

获取特定会话的历史消息记录。

- **URL**: `/api/history`
- **方法**: `POST`
- **Content-Type**: `application/json`

**请求参数**:

```json
{
  "session_id": "会话ID"
}
```

**响应**:

```json
{
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "你好",
      "created_at": "2023-06-01T12:00:00.000Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "你好！有什么我可以帮助你的吗？",
      "created_at": "2023-06-01T12:00:05.000Z"
    }
  ]
}
```

**状态码**:

- `200 OK`: 请求成功
- `500 Internal Server Error`: 服务器错误

### 4. 健康检查

检查 API 服务是否正常运行。

- **URL**: `/api/health`
- **方法**: `GET`

**响应**:

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

**状态码**:

- `200 OK`: 服务正常运行

## 客户端集成示例

### JavaScript 示例 (非流式)

```javascript
async function sendMessage(message) {
  try {
    const response = await fetch('http://localhost:3004/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: [
          { role: 'user', content: message }
        ],
        session_id: 'your-session-id' // 可选
      }),
    });
    
    const data = await response.json();
    return data.content;
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}
```

### JavaScript 示例 (流式)

```javascript
async function streamMessage(messages, sessionId, onChunk, onComplete, onError) {
  try {
    const response = await fetch('http://localhost:3004/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messages,
        session_id: sessionId
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        onComplete();
        break;
      }
      
      buffer += decoder.decode(value, { stream: true });
      
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || '';
      
      for (const line of lines) {
        if (line.startsWith('data:')) {
          const data = line.slice(5).trim();  // 去除 "data:" 前缀
          if (data) {
            onChunk(data);
          }
        } else if (line.includes('event: done')) {
          onComplete();
        } else if (line.includes('event: error')) {
          onError(new Error(line));
        }
      }
    }
  } catch (error) {
    onError(error);
  }
}
```

### 前端实现注意事项

前端实现时需要注意以下几点：

1. **处理会话ID**：每个用户会话应该有一个唯一的会话ID，可以存储在本地存储(localStorage)中
2. **历史记录加载**：页面加载时应该加载历史消息记录
3. **流式响应处理**：使用流式响应API可以实现打字机效果，提升用户体验
4. **错误处理**：实现适当的错误处理机制，包括网络错误、API错误等
5. **UI设计**：为用户和助手消息提供清晰的区分

## 后端实现说明

后端使用了以下技术：

- **FastAPI**：高性能的Python web框架
- **SQLite**：轻量级关系型数据库，存储聊天历史
- **SQLAlchemy**：数据库ORM工具
- **SSE**：服务器发送事件，用于流式响应
- **Requests**：HTTP客户端库，用于与Deepseek API通信

Deepseek API的集成使用了requests库，不需要依赖openai库。主要实现方式是向Deepseek API发送标准的HTTP请求，并处理返回的响应。

对于流式响应，我们解析返回的SSE格式数据，将每个增量部分发送给客户端。流式响应的处理是通过读取响应行并解析`data:`前缀的内容实现的。