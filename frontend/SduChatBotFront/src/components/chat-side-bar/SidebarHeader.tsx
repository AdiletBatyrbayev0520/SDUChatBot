import React from 'react';

interface SidebarHeaderProps {
    onCollapse: () => void;
}

const SidebarHeader: React.FC<SidebarHeaderProps> = ({ onCollapse }) => {
    return (
        <div className="flex items-center justify-between ml-4">
            <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center overflow-hidden">
                    <img 
                        src="https://sdu-chatbot-front-elements.s3.eu-central-1.amazonaws.com/sdu_logo+(1).jpg"
                        alt="SDU Logo"
                        className="w-full h-full object-cover"
                    />
                </div>
                <div>
                    <h1 className="text-lg font-semibold text-gray-900">SDU Chat</h1>
                    <p className="text-xs text-gray-500">Knowledge Base</p>
                </div>
            </div>
            <button
                onClick={onCollapse}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors"
            >
                <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
                    />
                </svg>
            </button>
        </div>
    );
};

export default SidebarHeader; 