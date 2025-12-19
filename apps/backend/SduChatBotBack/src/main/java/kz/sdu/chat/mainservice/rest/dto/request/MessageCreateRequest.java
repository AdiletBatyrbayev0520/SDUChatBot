package kz.sdu.chat.mainservice.rest.dto.request;

import lombok.Data;

@Data
public class MessageCreateRequest {
    private String content;
}
