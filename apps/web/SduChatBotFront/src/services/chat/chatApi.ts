import {baseApi} from "../baseApi.ts";
import type {PaginatedResponse} from "@/services/baseTypes.ts";
import type {Chat, Message, SendMessageResponse} from "@/services/chat/types.ts";


export const chatApi = baseApi.injectEndpoints({
    endpoints: (builder) => ({
        checkConnection: builder.query<boolean, void>({
            query: () => ({
                url: '/chats/connected',
                method: 'GET',
            }),
        }),
        getChats: builder.query<PaginatedResponse<Chat>, { page: number; size: number }>({
            query: ({page, size}) => ({
                url: `/chats`,
                method: 'GET',
                params: {page, size},
            }),
        }),
        getChat: builder.query<Chat, { chatId: number }>({
            query: ({chatId}) => ({
                url: `/chats/${chatId}`,
                method: 'GET'
            }),
        }),
        getMessages: builder.query<PaginatedResponse<Message>, { chatId: number; page: number; size: number }>({
            query: ({chatId, page, size}) => ({
                url: `/chats/${chatId}/messages`,
                method: 'GET',
                params: {page, size},
            }),
        }),
        sendMessage: builder.mutation<SendMessageResponse, { chatId: number, content: string }>({
            query: ({chatId, content}) => ({
                url: `/chats/${chatId}/messages`,
                method: 'POST',
                body: {content},
            }),
        }),
        sendInitialMessage: builder.mutation<SendMessageResponse, { content: string }>({
            query: ({content}) => ({
                url: `/chats/send-message`,
                method: 'POST',
                body: {content},
            }),
        }),
        deleteChat: builder.mutation<void, { chatId: number }>({
            query: ({chatId}) => ({
                url: `/chats/${chatId}`,
                method: 'DELETE',
            }),
        }),
    }),
});

export const {
    useCheckConnectionQuery,
    useLazyGetMessagesQuery,
    useLazyGetChatsQuery,
    useSendMessageMutation,
    useLazyGetChatQuery,
    useSendInitialMessageMutation,
    useDeleteChatMutation
} = chatApi;