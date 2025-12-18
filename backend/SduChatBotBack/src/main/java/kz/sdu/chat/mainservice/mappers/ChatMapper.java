package kz.sdu.chat.mainservice.mappers;

import kz.sdu.chat.mainservice.entities.Chat;
import kz.sdu.chat.mainservice.entities.User;
import kz.sdu.chat.mainservice.rest.dto.request.ChatCreateRequest;
import kz.sdu.chat.mainservice.rest.dto.response.ChatResponse;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface ChatMapper {
    ChatResponse toResponse(Chat chat);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "title", source = "chatCreateRequest.title")
    @Mapping(target = "owner", source = "user")
    Chat toEntity(ChatCreateRequest chatCreateRequest, User user);
}
