import React, { useState, useEffect, useRef } from 'react';
import Message from './Message';
import ChatInput from './ChatInput';
import { Message as MessageType } from '../types';
import { fetchChatHistory, sendChatMessageWithSSE } from '../services/api';

const ChatContainer: React.FC = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 从本地存储加载会话ID
  useEffect(() => {
    const storedSessionId = localStorage.getItem('chatSessionId');
    if (storedSessionId) {
      setSessionId(storedSessionId);
      loadChatHistory(storedSessionId);
    } else {
      // 创建新的会话ID
      const newSessionId = `session_${Date.now()}`;
      setSessionId(newSessionId);
      localStorage.setItem('chatSessionId', newSessionId);
    }
  }, []);

  // 滚动到最新消息
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // 加载聊天历史
  const loadChatHistory = async (sid: string) => {
    try {
      const historyMessages = await fetchChatHistory(sid);
      setMessages(historyMessages);
    } catch (err) {
      console.error('加载历史记录错误:', err);
      setError('无法加载聊天历史记录');
    }
  };

  // 清除所有聊天记录
  const clearChatHistory = () => {
    if (!sessionId) return;
    
    // 确认用户是否真的要清除聊天
    if (window.confirm('确定要清除所有聊天记录吗？此操作不可恢复。')) {
      // 清空消息数组
      setMessages([]);
      
      // 创建一个新的会话ID
      const newSessionId = `session_${Date.now()}`;
      setSessionId(newSessionId);
      localStorage.setItem('chatSessionId', newSessionId);
    }
  };

  // 发送消息并处理流式响应
  const handleSendMessage = async (content: string) => {
    if (!sessionId) return;
    
    setIsLoading(true);
    setError(null);
    
    // 添加用户消息到聊天
    const userMessage: MessageType = { role: 'user', content };
    setMessages((prev: MessageType[]) => [...prev, userMessage]);
    
    // 创建空的助手消息
    const assistantMessage: MessageType = { role: 'assistant', content: '' };
    setMessages((prev: MessageType[]) => [...prev, assistantMessage]);
    
    try {
      const allMessages = [
        { role: 'system' as const, content: '你是一个有用的助手' },
        ...messages.filter((m: MessageType) => m.role !== 'system'),
        userMessage,
      ];
      
      // 使用EventSource API处理SSE
      const cancelSSE = sendChatMessageWithSSE(
        allMessages,
        sessionId,
        // onMessage回调
        (responseText) => {
          setMessages((prev: MessageType[]) => 
            prev.map((m, i) => 
              i === prev.length - 1 ? { ...m, content: responseText } : m
            )
          );
        },
        // onError回调
        (error) => {
          console.error('SSE错误:', error);
          setError('发送消息失败，请重试');
          setMessages((prev: MessageType[]) => prev.slice(0, -1));
        },
        // onComplete回调
        () => {
          console.log('SSE传输完成');
          setIsLoading(false);
        }
      );
      
      // 如果组件卸载或请求取消，需要清理SSE连接
      return () => {
        cancelSSE();
      };
    } catch (err) {
      console.error('发送消息错误:', err);
      setError('发送消息失败，请重试');
      
      // 移除错误的助手消息
      setMessages((prev: MessageType[]) => prev.slice(0, -1));
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <header className="bg-primary text-white p-4 flex justify-between items-center shadow-md">
        <h1 className="text-2xl font-bold">Deepseek 聊天机器人</h1>
        <button 
          onClick={clearChatHistory}
          className="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded-md text-sm"
          disabled={messages.length === 0 || isLoading}
        >
          清除对话
        </button>
      </header>
      
      <main className="flex-1 overflow-auto py-4">
        <div className="chat-container">
          {error && (
            <div className="bg-red-100 text-red-700 p-3 rounded-md mb-4">
              {error}
            </div>
          )}
          
          <div className="message-container">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 my-8">
                发送消息开始聊天
              </div>
            ) : (
              messages.map((message: MessageType, index: number) => (
                <Message
                  key={index}
                  content={message.content}
                  role={message.role === 'user' ? 'user' : 'assistant'}
                />
              ))
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </main>
      
      <ChatInput
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
};

export default ChatContainer;