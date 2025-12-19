import { useNavigate } from "react-router";
import type {FC} from "react";


interface CreateNewChatProps {
    onCollapse: () => void;
}

const CreateNewChat:FC<CreateNewChatProps> = ({onCollapse}) => {
    const navigate = useNavigate()
    return (
        <div className="">
            <button
                onClick={() => {
                    navigate("/");
                    onCollapse();
                }}
                className="w-full flex items-center justify-start px-4 py-2 text-black rounded-lg hover:bg-gray-200 transition-colors cursor-pointer"
            >
                <svg
                    className="w-5 h-5 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 4v16m8-8H4"
                    />
                </svg>
                Новый чат
            </button>
        </div>
    );
}

export default CreateNewChat;