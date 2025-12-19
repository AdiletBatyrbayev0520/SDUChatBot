export interface Chat {
    id: number;
    title: string;
    createdDate?: string;
}

export interface Message {
    id: number;
    content: string;
    sources: string[] | null;
    number: number;
    version: number;
    createdDate: string;
    user: boolean;
}

export interface SendMessageResponse {
    messageResponse: Message;
    chatId?: number;
    title?: string;
}
