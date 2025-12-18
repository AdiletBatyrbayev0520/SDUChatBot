package kz.sdu.chat.mainservice.services;

import kz.sdu.chat.mainservice.entities.User;
import kz.sdu.chat.mainservice.rest.dto.request.ChatCreateRequest;
import kz.sdu.chat.mainservice.rest.dto.response.ChatResponse;
import kz.sdu.chat.mainservice.rest.dto.base.PaginationParams;
import org.springframework.data.domain.Page;

public interface ChatService {
    Page<ChatResponse> getChats(User user, PaginationParams paginationParams);

    void createChat(ChatCreateRequest chatCreateRequest, User user);

    void deleteChat(long chatId, User user);

    Object getConnectionStatus();

    ChatResponse getChatById(long chatId, User user);
}
