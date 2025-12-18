import React from 'react';
import type { Chat } from "@/services/chat/types.ts";

interface ChatHeaderProps {
    chat: Chat;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({ chat }) => {
    return (
        <div className="p-4 border-b border-gray-200 bg-white shadow-sm">
            <h1 className="text-xl font-semibold text-gray-900">
                {chat.title}
            </h1>
        </div>
    );
};

export default ChatHeader; 