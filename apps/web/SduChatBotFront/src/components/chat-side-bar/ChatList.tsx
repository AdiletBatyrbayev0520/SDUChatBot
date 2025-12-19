import {useEffect, useRef, useState} from "react";
import {useLazyGetChatsQuery, useDeleteChatMutation} from "@/services/chat/chatApi.ts";
import {useNavigate, useSearchParams} from "react-router";
import {useDispatch, useSelector} from "react-redux";
import type {RootState} from "@/store/store.ts";
import {setChats} from "@/store/chatSlice.ts";

const PAGE_SIZE = 100;

interface ChatItemProps {
    chat: {
        id: number;
        title: string;
    };
    onCollapse?: () => void;
    isActive: boolean;
    onNavigate: (chatId: number) => void;
    onDelete: (chatId: number, e: React.MouseEvent) => void;
}

const ChatDropdown = ({ chatId, onDelete, onClose }: { chatId: number; onDelete: (chatId: number, e: React.MouseEvent) => void; onClose: () => void }) => {
    const dropdownRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                onClose();
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [onClose]);

    return (
        <div 
            ref={dropdownRef}
            className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200"
            onClick={(e) => e.stopPropagation()}
        >
            <button
                onClick={(e) => onDelete(chatId, e)}
                className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
            >
                Удалить
            </button>
        </div>
    );
};

const ChatItem = ({ chat, isActive, onNavigate, onDelete, onCollapse }: ChatItemProps) => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    return (
        <div
            className={`cursor-pointer hover:bg-gray-50 relative py-2 px-4 px-1 rounded-md ${
                isActive ? 'bg-gray-100' : ''
            }`}
            onClick={() => {
                if (isActive) return;
                onNavigate(chat.id);
                if (onCollapse) {
                    onCollapse();
                }
            }}
        >
            <div className="flex justify-between items-start">
                <h3 className="font-medium text-gray-900">{chat.title}</h3>
                <div className="relative">
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            setIsDropdownOpen(!isDropdownOpen);
                        }}
                        className="p-1 hover:bg-gray-200 rounded-full"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                        </svg>
                    </button>
                    {isDropdownOpen && (
                        <ChatDropdown 
                            chatId={chat.id} 
                            onDelete={onDelete} 
                            onClose={() => setIsDropdownOpen(false)}
                        />
                    )}
                </div>
            </div>
        </div>
    );
};

const useInfiniteScroll = (hasMore: boolean, onLoadMore: () => void) => {
    const loader = useRef<HTMLDivElement | null>(null);
    const isFetchingRef = useRef(false);

    useEffect(() => {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && hasMore && !isFetchingRef.current) {
                onLoadMore();
            }
        }, {threshold: 1});

        if (loader.current) observer.observe(loader.current);

        return () => {
            if (loader.current) observer.unobserve(loader.current);
        };
    }, [hasMore, onLoadMore]);

    return { loader, isFetchingRef };
};

interface ChatListSidebarProps {
    onCollapse?: () => void;
}

const ChatList = ({onCollapse}:ChatListSidebarProps) => {
    const dispatch = useDispatch();
    const chats = useSelector((state: RootState) => state.chat.chats);
    const [page, setPage] = useState(0);
    const [hasMore, setHasMore] = useState(true);
    const [trigger, {isLoading}] = useLazyGetChatsQuery();
    const [deleteChat] = useDeleteChatMutation();
    const chatId = useSearchParams()[0].get('chatId');
    const navigate = useNavigate();

    const fetchChats = async (pageToLoad: number) => {
        isFetchingRef.current = true;
        const result = await trigger({page: pageToLoad, size: PAGE_SIZE}, true);
        if ('data' in result && result.data) {
            const {content, page: resultPage, totalPages} = result.data;
            if (content) {
                if (pageToLoad === 0) {
                    dispatch(setChats(content));
                } else {
                    dispatch(setChats([...chats, ...content]));
                }
                setHasMore(resultPage + 1 < totalPages);
                setPage(resultPage);
            }
        }
        isFetchingRef.current = false;
    };

    const { loader, isFetchingRef } = useInfiniteScroll(hasMore, () => fetchChats(page + 1));

    useEffect(() => {
        if (chats.length === 0 && !isFetchingRef.current) {
            fetchChats(0);
        }
    }, [chats.length]);

    useEffect(() => {
        if (chatId) {
            fetchChats(0);
        }
    }, [chatId]);

    const handleDeleteChat = async (chatId: number, e: React.MouseEvent) => {
        e.stopPropagation();
        try {
            await deleteChat({ chatId }).unwrap();
            dispatch(setChats(chats.filter(chat => chat.id !== chatId)));
            if (chatId === Number(chatId)) {
                navigate('/');
            }
        } catch (error) {
            console.error('Failed to delete chat:', error);
        }
    };

    return (
        <div className="flex-1 h-full">
            {[...chats].reverse().map((chat) => (
                <ChatItem
                    key={chat.id}
                    chat={chat}
                    onCollapse={onCollapse}
                    isActive={(chatId && +chatId) === chat.id}
                    onNavigate={(id) => navigate(`/${id}`)}
                    onDelete={handleDeleteChat}
                />
            ))}
            <div ref={loader}/>
            {isLoading && <div className="p-4 text-center text-gray-500">Загрузка...</div>}
        </div>
    );
};

export default ChatList;