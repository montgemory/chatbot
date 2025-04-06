import uuid
import logging
from typing import List
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse
import json

from .database import get_db, create_tables, ChatMessage
from .deepseek_client import DeepseekClient
from .models import ChatRequest, ChatResponse, SessionHistoryRequest, SessionHistoryResponse, HistoryMessage

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(title="Deepseek 聊天机器人 API")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3007", 
        "http://localhost:8080",  
        "https://chatbot-backend-production-4462.up.railway.app"
    ],  # 允许前端地址访问
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建 Deepseek 客户端
deepseek_client = DeepseekClient()

# 启动时创建数据库表
@app.on_event("startup")
def startup_event():
    logger.info("创建数据库表...")
    create_tables()
    logger.info("数据库表创建完成")

# 保存消息到数据库的函数
def save_message(db: Session, session_id: str, role: str, content: str):
    db_message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# 聊天 API 端点
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # 生成或使用现有会话 ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # 获取消息
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # 记录用户消息
        if messages and messages[-1]["role"] == "user":
            save_message(db, session_id, "user", messages[-1]["content"])
        
        # 发送到 Deepseek API
        if not request.stream:
            response = deepseek_client.chat_completion(messages)
            content = response["choices"][0]["message"]["content"]
            
            # 保存助手回复
            save_message(db, session_id, "assistant", content)
            
            return ChatResponse(content=content)
        else:
            # 对于流式请求，返回 500 错误，因为应该使用 /api/chat/stream 端点
            raise HTTPException(status_code=500, detail="流式请求应使用 /api/chat/stream 端点")
            
    except Exception as e:
        logger.error(f"聊天请求失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 流式聊天 API 端点
@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        # 生成或使用现有会话 ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # 获取消息
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # 记录用户消息
        if messages and messages[-1]["role"] == "user":
            save_message(db, session_id, "user", messages[-1]["content"])
        
        # 收集完整响应用于保存
        full_response = ""
        
        async def event_generator():
            nonlocal full_response
            try:
                response_stream = deepseek_client.generate_stream_response(messages)
                for content in response_stream:
                    full_response += content
                    # 使用标准SSE格式
                    yield {
                        "event": "message",
                        "id": str(uuid.uuid4()),
                        "data": content
                    }
                
                # 发送结束事件
                yield {
                    "event": "done",
                    "id": str(uuid.uuid4()),
                    "data": ""
                }
            except Exception as e:
                logger.error(f"流式生成失败: {str(e)}")
                yield {
                    "event": "error",
                    "id": str(uuid.uuid4()),
                    "data": str(e)
                }
        
        # 在流式响应完成后保存消息
        async def save_response():
            try:
                if full_response:
                    save_message(db, session_id, "assistant", full_response)
            except Exception as e:
                logger.error(f"保存响应失败: {str(e)}")
        
        background_tasks.add_task(save_response)
        
        return EventSourceResponse(event_generator())
            
    except Exception as e:
        logger.error(f"流式聊天请求失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 流式聊天 API 端点 (支持GET请求的SSE)
@app.get("/api/chat/stream/sse")
async def chat_stream_sse(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        # 从URL查询参数获取数据
        data_str = request.query_params.get('data')
        if not data_str:
            raise HTTPException(status_code=400, detail="缺少必要的数据参数")
        
        # 解析JSON数据
        data = json.loads(data_str)
        session_id = data.get('session_id') or str(uuid.uuid4())
        messages = data.get('messages', [])
        
        # 记录用户消息
        if messages and messages[-1]["role"] == "user":
            save_message(db, session_id, "user", messages[-1]["content"])
        
        # 收集完整响应用于保存
        full_response = ""
        
        async def event_generator():
            nonlocal full_response
            try:
                response_stream = deepseek_client.generate_stream_response(messages)
                for content in response_stream:
                    full_response += content
                    # 简化的SSE格式，直接发送内容
                    yield {"event": "message", "data": content}
                
                # 发送结束事件
                yield {"event": "done", "data": "[DONE]"}
            except Exception as e:
                logger.error(f"SSE流式生成失败: {str(e)}")
                yield {"event": "error", "data": str(e)}
        
        # 在流式响应完成后保存消息
        async def save_response():
            try:
                if full_response:
                    save_message(db, session_id, "assistant", full_response)
            except Exception as e:
                logger.error(f"保存响应失败: {str(e)}")
        
        background_tasks.add_task(save_response)
        
        return EventSourceResponse(
            event_generator(),
            media_type="text/event-stream",
            ping=10000  # 发送ping信号保持连接活跃
        )
            
    except Exception as e:
        logger.error(f"SSE流式聊天请求失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 获取会话历史记录
@app.post("/api/history", response_model=SessionHistoryResponse)
async def get_session_history(request: SessionHistoryRequest, db: Session = Depends(get_db)):
    try:
        # 查询会话历史记录
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == request.session_id
        ).order_by(ChatMessage.created_at.asc()).all()
        
        # 转换为响应模型
        history_messages = [
            HistoryMessage(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at.isoformat()
            )
            for msg in messages
        ]
        
        return SessionHistoryResponse(messages=history_messages)
            
    except Exception as e:
        logger.error(f"获取历史记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 健康检查端点
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"} 