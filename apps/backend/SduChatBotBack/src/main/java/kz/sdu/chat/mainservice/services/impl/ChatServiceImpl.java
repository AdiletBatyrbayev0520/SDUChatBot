package kz.sdu.chat.mainservice.services.impl;

import kz.sdu.chat.mainservice.entities.Chat;
import kz.sdu.chat.mainservice.entities.User;
import kz.sdu.chat.mainservice.exceptions.DbNotFoundException;
import kz.sdu.chat.mainservice.feign.sduai.SduAiAPI;
import kz.sdu.chat.mainservice.mappers.ChatMapper;
import kz.sdu.chat.mainservice.repositories.ChatRepository;
import kz.sdu.chat.mainservice.rest.dto.base.PaginationParams;
import kz.sdu.chat.mainservice.rest.dto.request.ChatCreateRequest;
import kz.sdu.chat.mainservice.rest.dto.response.ChatResponse;
import kz.sdu.chat.mainservice.services.ChatService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class ChatServiceImpl implements ChatService {
    private final ChatRepository chatRepository;
    private final ChatMapper chatMapper;
    private final SduAiAPI sduAiAPI;

    @Override
    public Page<ChatResponse> getChats(User user, PaginationParams paginationParams) {
        return chatRepository.findAllByOwnerId(user.getId(), paginationParams.toPageable())
                .map(chatMapper::toResponse);
    }

    @Override
    public void createChat(ChatCreateRequest chatCreateRequest, User user) {
        log.info("Creating chat with title: {}", chatCreateRequest.getTitle());
        var toCreate = chatMapper.toEntity(chatCreateRequest, user);
        var createdChat = chatRepository.save(toCreate);
        log.info("Chat created successfully with ID: {}", createdChat.getId());
    }

    @Override
    public void deleteChat(long chatId, User user) {
        log.info("Deleting chat with ID: {}", chatId);
        var chat = this.findChatById(chatId, user);
        chat.setDeleted(true);
        chatRepository.save(chat);
        log.info("Chat with ID: {} deleted successfully", chatId);
    }

    @Override
    public Object getConnectionStatus() {
        return sduAiAPI.getConnectionStatus();
    }

    @Override
    public ChatResponse getChatById(long chatId, User user) {
        var chat = chatRepository.findById(chatId)
                .orElseThrow(() -> new DbNotFoundException(HttpStatus.NOT_FOUND, "Chat not found", ""));

        if (chat.getOwner().getId() != user.getId()) {
            throw new DbNotFoundException(HttpStatus.NOT_FOUND, "Chat not found", "");
        }

        return chatMapper.toResponse(chat);
    }

    private Chat findChatById(long chatId, User user) {
        return chatRepository.findById(chatId)
                .filter(chat -> chat.getOwner().getId() == user.getId() && !chat.isDeleted())
                .orElseThrow(() -> new DbNotFoundException(HttpStatus.NOT_FOUND, "Chat not found", ""));
    }
}
