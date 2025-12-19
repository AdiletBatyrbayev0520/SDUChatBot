package kz.sdu.chat.mainservice.services.impl;

import kz.sdu.chat.mainservice.entities.Chat;
import kz.sdu.chat.mainservice.entities.User;
import kz.sdu.chat.mainservice.exceptions.DbNotFoundException;
import kz.sdu.chat.mainservice.feign.sduai.SduAiAPI;
import kz.sdu.chat.mainservice.feign.sduai.dto.ChatMessageSendRequest;
import kz.sdu.chat.mainservice.mappers.MessageMapper;
import kz.sdu.chat.mainservice.repositories.ChatRepository;
import kz.sdu.chat.mainservice.repositories.MessageRepository;
import kz.sdu.chat.mainservice.rest.dto.base.PaginationParams;
import kz.sdu.chat.mainservice.rest.dto.request.MessageCreateRequest;
import kz.sdu.chat.mainservice.rest.dto.response.MessageResponse;
import kz.sdu.chat.mainservice.rest.dto.response.SendMessageResponse;
import kz.sdu.chat.mainservice.services.MessageService;
import kz.sdu.chat.mainservice.services.MessageTokenService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class MessageServiceImpl implements MessageService {
    private final MessageRepository messageRepository;
    private final MessageMapper messageMapper;
    private final ChatRepository chatRepository;
    private final SduAiAPI sduAiAPI;
    private final MessageTokenService messageTokenService;


    @Override
    public Page<MessageResponse> getMessagesForChat(long chatId, User user, PaginationParams paginationParams) {
        var chat = this.findChatById(chatId, user);

        Pageable pageable = PageRequest.of(paginationParams.getPage(), paginationParams.getSize(), Sort.by(Sort.Direction.DESC, "createdDate"));

        return messageRepository.findAllByChatId(chatId, pageable)
                .map(messageMapper::toResponse);
    }

    @Override
    public SendMessageResponse sendMessage(long chatId, MessageCreateRequest messageCreateRequest, User user) {
        messageTokenService.checkMessageToken(user);
        
        var chat = this.findChatById(chatId, user);

        var ans = sduAiAPI.sendMessage(ChatMessageSendRequest.builder()
                .question(messageCreateRequest.getContent())
                .chat_id(chat.getUniqueUUID())
                .is_need_topic(true)
                .build());
        var aiMessageEntity = messageMapper.toEntity(ans, chat);
        var messageResponseFromAi = messageMapper.toResponse(aiMessageEntity);
        messageResponseFromAi.setCreatedDate(LocalDateTime.now().toString());

        var messages = List.of(messageMapper.toEntity(messageCreateRequest, chat, user), aiMessageEntity);
        messageRepository.saveAll(messages);

        messageTokenService.addtokenToUser(user, ans.getUsage_metadata().getCostUsd());

        return SendMessageResponse.builder()
                .chatId(chatId)
                .messageResponse(messageResponseFromAi)
                .title(chat.getTitle())
                .build();
    }

    @Override
    public SendMessageResponse createChatAndSendMessage(MessageCreateRequest messageCreateRequest, User user) {
        messageTokenService.checkMessageToken(user);
        
        var chat = createChat(user);
        var ans = sduAiAPI.sendMessage(ChatMessageSendRequest.builder()
                .question(messageCreateRequest.getContent())
                .chat_id(chat.getUniqueUUID())
                .is_need_topic(true)
                .build());
        var aiMessageEntity = messageMapper.toEntity(ans, chat);
        var messageResponseFromAi = messageMapper.toResponse(aiMessageEntity);
        messageResponseFromAi.setCreatedDate(LocalDateTime.now().toString());
        setChatTitle(chat.getId(), ans.getTopic());

        var messages = List.of(messageMapper.toEntity(messageCreateRequest, chat, user), aiMessageEntity);

        messageRepository.saveAll(messages);
        messageTokenService.addtokenToUser(user, ans.getUsage_metadata().getCostUsd());

        return SendMessageResponse.builder()
                .chatId(chat.getId())
                .messageResponse(messageResponseFromAi)
                .title(chat.getTitle())
                .build();
    }

    private Chat createChat(User user) {
        var chat = new Chat();
        chat.setTitle("");
        chat.setOwner(user);
        return chatRepository.save(chat);
    }

    private void setChatTitle(Long id, String title){
        var chat = chatRepository.findById(id).orElseThrow(() -> new DbNotFoundException(HttpStatus.NOT_FOUND, "Chat not found", ""));
        chat.setTitle(title);
        chatRepository.save(chat);
    }

    private Chat findChatById(long chatId, User user) {
        return chatRepository.findById(chatId)
                .filter(chat -> chat.getOwner().getId() == user.getId() && !chat.isDeleted())
                .orElseThrow(() -> new DbNotFoundException(HttpStatus.NOT_FOUND, "Chat not found", ""));
    }
}
