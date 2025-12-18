import type {FC} from 'react';
import {useSelector} from 'react-redux';
import type {RootState} from '../store/store';
import {useNavigate} from 'react-router';
import ChatSidebar from '../components/chat-side-bar/ChatSidebar.tsx';
import ChatComponent from '../components/chat/Chat.tsx';
import {useState} from 'react';

const MainPage: FC = () => {
    const navigate = useNavigate();
    const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    if (!isAuthenticated) {
        navigate('/login');
        return null;
    }

    return (
        <div className="flex h-[100dvh] bg-gray-100">
            {/* Sidebar for larger screens */}
            <div className="hidden lg:block w-80">
                <ChatSidebar onCollapse={() => setIsSidebarOpen(false)} />
            </div>

            {/* Sidebar for mobile (drawer) */}
            <div
                className={`absolute inset-y-0 left-0 z-30 w-80 bg-white transition-transform duration-300 ease-in-out transform ${
                    isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
                } lg:hidden`}
            >
                <ChatSidebar onCollapse={() => setIsSidebarOpen(false)} />
            </div>

            {/* Overlay for mobile */}
            {isSidebarOpen && (
                <div
                    className="fixed inset-0 z-20 bg-black opacity-50 lg:hidden"
                    onClick={() => setIsSidebarOpen(false)}
                ></div>
            )}

            <div className="flex-1 flex flex-col">
                <button
                    onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                    className="lg:hidden absolute top-4 left-4 z-10 p-2 rounded-md bg-white shadow-md hover:bg-gray-50 transition-colors"
                >
                    <svg
                        className="w-6 h-6 text-gray-600"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M4 6h16M4 12h16M4 18h16"
                        />
                    </svg>
                </button>
                <ChatComponent />
            </div>
        </div>
    );
};

export default MainPage; 