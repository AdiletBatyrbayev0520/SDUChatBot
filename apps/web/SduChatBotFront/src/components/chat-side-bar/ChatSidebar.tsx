import ConnectionStatus from "./ConnectionStatus.tsx";
import AccountInfo from "./AccountInfo.tsx";
import ChatList from "@/components/chat-side-bar/ChatList.tsx";
import CreateNewChat from "@/components/chat-side-bar/CreateNewChat.tsx";
import SidebarHeader from "./SidebarHeader.tsx";

interface ChatSidebarProps {
    onCollapse: () => void;
}

const ChatSidebar: React.FC<ChatSidebarProps> = ({onCollapse}) => {
    return (
        <div className="w-80 bg-white border-r border-gray-200 flex flex-col h-[100dvh]">
            <div className="flex-1 flex flex-col gap-8 overflow-y-auto mt-4  min-h-0">
                <div className="flex flex-col gap-2">
                    <SidebarHeader onCollapse={onCollapse}/>
                    <CreateNewChat onCollapse={onCollapse}/>
                </div>
                <div className={"flex flex-col gap-2"}>
                    <ConnectionStatus/>
                    <ChatList onCollapse={onCollapse}/>
                </div>
            </div>
            <AccountInfo/>
        </div>
    );
};

export default ChatSidebar; 