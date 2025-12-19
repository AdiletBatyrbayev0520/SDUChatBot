package kz.sdu.chat.mainservice.services;

import kz.sdu.chat.mainservice.entities.User;
import kz.sdu.chat.mainservice.rest.dto.base.PaginationParams;
import kz.sdu.chat.mainservice.rest.dto.request.MessageCreateRequest;
import kz.sdu.chat.mainservice.rest.dto.response.MessageResponse;
import kz.sdu.chat.mainservice.rest.dto.response.SendMessageResponse;
import org.springframework.data.domain.Page;

public interface MessageService {
    Page<MessageResponse> getMessagesForChat(long chatId, User user, PaginationParams paginationParams);

    SendMessageResponse sendMessage(long chatId, MessageCreateRequest messageCreateRequest, User user);

    SendMessageResponse createChatAndSendMessage(MessageCreateRequest messageCreateRequest, User user);
}
