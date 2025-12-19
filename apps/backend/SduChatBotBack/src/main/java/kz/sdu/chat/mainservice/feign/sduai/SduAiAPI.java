package kz.sdu.chat.mainservice.feign.sduai;

import kz.sdu.chat.mainservice.config.ApplicationProperties;
import kz.sdu.chat.mainservice.feign.sduai.dto.ChatAnswerResponse;
import kz.sdu.chat.mainservice.feign.sduai.dto.ChatMessageSendRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
@RequiredArgsConstructor
@Slf4j
public class SduAiAPI {

    private final ApplicationProperties properties;
    private final RestTemplate restTemplate = new RestTemplate(); // локальное поле

    public ChatAnswerResponse sendMessage(ChatMessageSendRequest messageCreateRequest) {
        HttpHeaders headers = new HttpHeaders();

        // log.info("Using API Key: {}", properties.getSduAiApiKey()); // закомментировано для безопасности
//        headers.set("API-KEY", properties.getSduAiApiKey());

        HttpEntity<ChatMessageSendRequest> request = new HttpEntity<>(messageCreateRequest, headers);

        log.info("Sending request to SDU AI API: URL={}, Payload={}", properties.getSduAiApiUrl(), messageCreateRequest);

        try {
            ChatAnswerResponse response = restTemplate.postForObject(
                    properties.getSduAiApiUrl(),
                    request,
                    ChatAnswerResponse.class
            );

            log.info("Received response from SDU AI API: {}", response);
            return response;

        } catch (Exception e) {
            log.error("Error while sending request to SDU AI API", e);
            throw e;
        }
    }

    public Object getConnectionStatus() {
        log.info("Checking connection status with SDU AI API at URL: {}", properties.getSduAiApiUrl());
        try {
            var status = restTemplate.getForObject(properties.getSduAiApiUrl(), Object.class);
            log.info("Connection status: {}", status);
            return status;
        } catch (Exception e) {
            log.error("Error while checking connection status with SDU AI API", e);
            throw e;
        }
    }
}

