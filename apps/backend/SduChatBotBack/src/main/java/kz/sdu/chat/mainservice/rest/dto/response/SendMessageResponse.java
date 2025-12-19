package kz.sdu.chat.mainservice.rest.dto.response;

import lombok.Builder;
import lombok.Data;


@Data
@Builder
public class SendMessageResponse {
    private long chatId;
    private String title;
    private MessageResponse messageResponse;
    private String createdDate;
}
