import React from 'react';
import MessageInput from './MessageInput';
import MessageBubble from './MessageBubble';
import type { Message } from "@/services/chat/types.ts";

interface WelcomeScreenProps {
    messages: Message[];
    message: string;
    setMessage: (message: string) => void;
    handleSubmit: (e: React.FormEvent) => void;
    isSending: boolean;
}

export const WelcomeScreen: React.FC<WelcomeScreenProps> = ({
    messages,
    message,
    setMessage,
    handleSubmit,
    isSending
}) => {
    if (messages.length > 0) {
        return (
            <div className="w-full max-w-3xl mx-auto flex flex-col h-full">
                <div className="flex-1 overflow-y-auto py-4 space-y-4">
                    {[...messages].reverse().map((message) => (
                        <MessageBubble key={message.id} message={message}/>
                    ))}
                </div>
                <div className="p-4 mt-auto">
                    <MessageInput
                        message={message}
                        setMessage={setMessage}
                        handleSubmit={handleSubmit}
                        isSending={isSending}
                    />
                </div>
            </div>
        );
    }

    const backgroundImage = "https://sdu-chatbot-front-elements.s3.eu-central-1.amazonaws.com/logo-1024x1016.png";

    return (
        <div className="w-full max-w-3xl mx-auto flex flex-col h-full">
            <div className="flex-1 flex flex-col items-center justify-center relative">
                <div 
                    style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        backgroundImage: `url(${backgroundImage})`,
                        backgroundSize: 'min(250px, 40vw) min(250px, 40vw)',
                        backgroundPosition: `center calc(50% - ${0 * 0}px)`,
                        backgroundRepeat: 'no-repeat',
                        opacity: 0.20,
                        pointerEvents: 'none',
                        zIndex: 1,
                        willChange: 'background-position',
                        transition: 'background-position 0.1s ease-out'
                    }}
                    className="sm:opacity-10"
                />
            </div>
            <div className="p-4 mt-auto">
                <MessageInput
                    message={message}
                    setMessage={setMessage}
                    handleSubmit={handleSubmit}
                    isSending={isSending}
                    placeholder="Задайте вопрос о СДУ..."
                />
            </div>
        </div>
    );
};

export default WelcomeScreen; 