import React from 'react';

interface MessageProps {
  content: string;
  role: 'user' | 'assistant';
}

const Message: React.FC<MessageProps> = ({ content, role }: MessageProps) => {
  return (
    <div className={`message ${role === 'user' ? 'user-message' : 'assistant-message'}`}>
      <p>{content}</p>
    </div>
  );
};

export default Message; 