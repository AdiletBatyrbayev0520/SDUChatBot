package kz.sdu.chat.mainservice.feign.google;

import kz.sdu.chat.mainservice.config.ApplicationProperties;
import kz.sdu.chat.mainservice.entities.User;
import kz.sdu.chat.mainservice.feign.google.dto.GoogleTokenResponse;
import kz.sdu.chat.mainservice.feign.google.dto.GoogleUserInfo;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.util.UUID;

@Component
@RequiredArgsConstructor
@Slf4j
public class GoogleAPI {

    private final ApplicationProperties properties;
    private final RestTemplate restTemplate = new RestTemplate(); // локальное поле

    public GoogleTokenResponse getOauthAccessTokenGoogle(String code) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

        MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
        body.add("code", code);
        body.add("redirect_uri", properties.getGoogleRedirectUri());
        body.add("client_id", properties.getGoogleClientId());
        body.add("client_secret", properties.getGoogleClientSecret());
        body.add("grant_type", "authorization_code");

        HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(body, headers);
        String url = "https://oauth2.googleapis.com/token";

        try {
            return restTemplate.postForObject(url, request, GoogleTokenResponse.class);
        } catch (Exception e) {
            log.error("Error exchanging Google OAuth code: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to get access token from Google", e);
        }
    }

    public User fetchGoogleUserProfile(String accessToken) {
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(accessToken);

        HttpEntity<Void> request = new HttpEntity<>(headers);
        String url = "https://www.googleapis.com/oauth2/v2/userinfo";

        try {
            ResponseEntity<GoogleUserInfo> response = restTemplate.exchange(
                    url, HttpMethod.GET, request, GoogleUserInfo.class
            );

            GoogleUserInfo info = response.getBody();
            if (info == null) {
                throw new IllegalStateException("Google user info is null");
            }

            return User.builder()
                    .email(info.getEmail())
                    .firstName(info.getGivenName())
                    .lastName(info.getFamilyName())
                    .password(UUID.randomUUID().toString())
                    .build();

        } catch (Exception e) {
            log.error("Error fetching Google user profile: {}", e.getMessage(), e);
            throw new RuntimeException("Failed to fetch user profile from Google", e);
        }
    }
}
