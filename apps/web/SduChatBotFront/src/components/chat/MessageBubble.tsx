import React from 'react';
import type { Message } from "@/services/chat/types.ts";
import TextFormatter from './TextFormatter';
import {AlertModal} from "@/components/chat/AlertModal.tsx";

const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const isToday = date.toDateString() === now.toDateString();

    if (isToday) {
        return date.toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
    }

    return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
};

interface MessageBubbleProps {
    message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({message}) => {
    const isUser = message.user;

    return (
        <div className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                isUser ? 'bg-blue-500' : 'bg-gray-200'
            }`}>
                <span className={`text-sm font-medium ${isUser ? 'text-white' : 'text-gray-600'}`}>
                    {isUser ? 'U' : 'AI'}
                </span>
            </div>

            <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-[70%]`}>
                <div className={`rounded-2xl px-4 py-2 ${
                    isUser
                        ? 'bg-blue-500 text-white rounded-tr-none'
                        : 'bg-gray-100 text-gray-800 rounded-tl-none'
                }`}>
                    {isUser ? (
                        <p className="whitespace-pre-wrap break-words">{message.content}</p>
                    ) : (
                        <TextFormatter text={message.content} className="leading-relaxed" />
                    )}
                </div>

                {message.sources && message.sources.length > 0 && (
                    <div className="mt-1 text-xs text-gray-500 max-w-full">
                        <div className="flex flex-wrap gap-1">
                            {message.sources.map((source, index) => (
                                <span key={index} className="bg-gray-100 px-2 py-1 rounded-full">
                                    <AlertModal link={source} text={source} />
                                </span>
                            ))}
                        </div>
                    </div>
                )}

                <span className="text-xs text-gray-500 mt-1">
                    {formatDate(message.createdDate)}
                </span>
            </div>
        </div>
    );
};

export default MessageBubble; 