package kz.sdu.chat.mainservice.rest.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class UsageMetadataResponse {
    private double costUsd;
}