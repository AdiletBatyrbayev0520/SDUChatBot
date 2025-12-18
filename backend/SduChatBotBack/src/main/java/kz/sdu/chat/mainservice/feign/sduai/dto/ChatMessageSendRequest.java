package kz.sdu.chat.mainservice.feign.sduai.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class ChatMessageSendRequest {
    private String question;
    private String chat_id;
    private Boolean is_need_topic;
}
