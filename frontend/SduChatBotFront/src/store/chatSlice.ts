import {createSlice} from "@reduxjs/toolkit";
import type {Chat} from "@/services/chat/types.ts";

interface ChatState {
    isConnected: boolean;
    chats: Chat[];
}

const initialState: ChatState = {
    isConnected: false,
    chats: [],
};

const chatSlice = createSlice({
    name: 'chat',
    initialState,
    reducers: {
        setConnectionStatus(state, action) {
            state.isConnected = action.payload;
        },
        setChats(state, action) {
            state.chats = action.payload;
        },
        addChat(state, action) {
            state.chats = [...state.chats, action.payload];
        },
        updateChat(state, action) {
            const index = state.chats.findIndex(chat => chat.id === action.payload.id);
            if (index !== -1) {
                state.chats[index] = action.payload;
            }
        }
    },
})

export const {setConnectionStatus, setChats, addChat, updateChat} = chatSlice.actions;
export default chatSlice.reducer;