# Deepseek 聊天机器人 - 后端服务

这是一个使用 Deepseek API 的聊天机器人后端服务，提供 REST API 接口与前端交互。

## 功能特性

- 使用 FastAPI 构建的高性能 API
- 集成 Deepseek 聊天 API
- 支持流式输出（SSE）
- 使用 SQLite 存储聊天历史
- 提供健康检查端点

## 安装

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 配置环境变量（已在 .env 文件中设置）：

```
DEEPSEEK_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./chatbot.db
```

## 运行服务

```bash
python run.py
```

默认情况下，服务器将在 http://localhost:3004 上运行。

## API 文档

服务启动后，可以在 http://localhost:3004/docs 查看完整的 API 文档。

### 主要端点

- `POST /api/chat` - 发送聊天请求（非流式）
- `POST /api/chat/stream` - 发送流式聊天请求 
- `POST /api/history` - 获取会话历史记录
- `GET /api/health` - 健康检查

## 开发说明

在开发模式下，服务启用了热重载功能，当代码变更时会自动重启服务。 