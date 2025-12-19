package kz.sdu.chat.mainservice.feign.sduai.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import kz.sdu.chat.mainservice.rest.dto.response.UsageMetadataResponse;
import lombok.Data;

import java.util.List;

@Data
public class ChatAnswerResponse {
    private String question;
    private String answer;
    private List<String> sources;
    private UsageMetadataResponse usage_metadata;
    private String topic;
}
