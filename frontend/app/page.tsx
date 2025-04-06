'use client';

import dynamic from 'next/dynamic';

// 使用动态导入以避免服务器端渲染时的localStorage错误
const ChatContainer = dynamic(() => import('../components/ChatContainer'), {
  ssr: false,
});

export default function Home() {
  return <ChatContainer />;
} 