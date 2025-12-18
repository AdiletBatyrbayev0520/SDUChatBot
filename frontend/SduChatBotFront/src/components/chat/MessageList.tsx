import React, { useRef } from 'react';
import type { Message } from "@/services/chat/types.ts";
import MessageBubble from './MessageBubble';

interface MessageListProps {
    messages: Message[];
    isLoading: boolean;
    onLoadMore: () => void;
    hasMore: boolean;
    isFetching: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({
    messages,
    isLoading,
    onLoadMore,
    hasMore,
    isFetching
}) => {
    const loadTriggerRef = useRef<HTMLDivElement>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const messagesContainerRef = useRef<HTMLDivElement>(null);

    React.useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                const [entry] = entries;
                if (entry.isIntersecting && hasMore && !isFetching) {
                    onLoadMore();
                }
            },
            {
                root: null,
                rootMargin: '100px',
                threshold: 0.1
            }
        );

        if (loadTriggerRef.current) {
            observer.observe(loadTriggerRef.current);
        }

        return () => {
            observer.disconnect();
        };
    }, [hasMore, isFetching, onLoadMore]);

    return (
        <div
            ref={messagesContainerRef}
            className="flex-1 py-4 overflow-y-auto space-y-4 px-4 w-full"
        >
            {isLoading && (
                <div className="flex justify-center py-2">
                    <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900"/>
                </div>
            )}
            <div ref={loadTriggerRef} className="h-4"/>
            <div className="max-w-3xl mx-auto w-full">
                {[...messages].reverse().map((message) => (
                    <MessageBubble key={message.id} message={message}/>
                ))}
            </div>
            <div ref={messagesEndRef}/>
        </div>
    );
};

export default MessageList; 