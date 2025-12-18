package kz.sdu.chat.mainservice.mappers;

import kz.sdu.chat.mainservice.entities.Chat;
import kz.sdu.chat.mainservice.entities.Message;
import kz.sdu.chat.mainservice.entities.User;
import kz.sdu.chat.mainservice.feign.sduai.dto.ChatAnswerResponse;
import kz.sdu.chat.mainservice.rest.dto.request.MessageCreateRequest;
import kz.sdu.chat.mainservice.rest.dto.response.MessageResponse;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface MessageMapper {
    @Mapping(target = "version", ignore = true)
    MessageResponse toResponse(Message message);

    @Mapping(target = "versions", ignore = true)
    @Mapping(target = "sources", ignore = true)
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "chat", source = "chat")
    @Mapping(target = "isUser", expression = "java(user != null)")
    @Mapping(target = "content", source = "messageCreateRequest.content")
    Message toEntity(MessageCreateRequest messageCreateRequest, Chat chat, User user);

    @Mapping(target = "versions", ignore = true)
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "chat", source = "chat")
    @Mapping(target = "isUser", expression = "java(false)")
    @Mapping(target = "content", source = "chatAnswerResponse.answer")
    @Mapping(target = "sources", source = "chatAnswerResponse.sources")
    @Mapping(target = "costUsd", source = "chatAnswerResponse.usage_metadata.costUsd")
    Message toEntity(ChatAnswerResponse chatAnswerResponse, Chat chat);
}