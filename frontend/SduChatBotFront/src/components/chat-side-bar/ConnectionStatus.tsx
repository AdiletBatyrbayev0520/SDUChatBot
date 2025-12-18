import {useCheckConnectionQuery} from "@/services/chat/chatApi.ts";
import {useEffect} from "react";
import {useDispatch} from "react-redux";
import {setConnectionStatus} from "@/store/chatSlice.ts";

interface StatusIndicatorProps {
    status: 'loading' | 'error' | 'connected' | 'disconnected';
}

const StatusIndicator = ({ status }: StatusIndicatorProps) => {
    const getStatusColor = () => {
        switch (status) {
            case 'loading':
                return 'bg-yellow-500';
            case 'error':
                return 'bg-red-500';
            case 'connected':
                return 'bg-green-500';
            case 'disconnected':
                return 'bg-red-500';
        }
    };

    const getStatusText = () => {
        switch (status) {
            case 'loading':
                return 'Loading...';
            case 'error':
                return 'Error';
            case 'connected':
                return 'Connected';
            case 'disconnected':
                return 'Disconnected';
        }
    };

    return (
        <div className="flex items-center">
            <div className={`w-2 h-2 rounded-full mr-2 ${getStatusColor()}`}/>
            <span className="text-sm text-gray-600">{getStatusText()}</span>
        </div>
    );
};

const ConnectionStatus = () => {
    const dispatch = useDispatch();
    const { data: isConnected, error, isLoading } = useCheckConnectionQuery();

    useEffect(() => {
        if (!isLoading && !error) {
            dispatch(setConnectionStatus(isConnected));
        }
    }, [isConnected, isLoading, error, dispatch]);

    const getStatus = (): StatusIndicatorProps['status'] => {
        if (isLoading) return 'loading';
        if (error) return 'error';
        return isConnected ? 'connected' : 'disconnected';
    };

    return (
        <div className="px-4">
            <div className="flex items-center justify-between">
                <h2 className="opacity-70 font-semibold">Чаты</h2>
                <StatusIndicator status={getStatus()} />
            </div>
        </div>
    );
};

export default ConnectionStatus;