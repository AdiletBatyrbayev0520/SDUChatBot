package kz.sdu.chat.mainservice.rest.dto.response;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class ChatResponse {
    private long id;
    private String title;
    private LocalDateTime createdDate;
}
