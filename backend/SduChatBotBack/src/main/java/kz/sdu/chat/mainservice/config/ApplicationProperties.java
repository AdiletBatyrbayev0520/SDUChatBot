package kz.sdu.chat.mainservice.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties
@Getter
@Setter
public class ApplicationProperties {
    private String googleClientId;
    private String googleClientSecret;
    private String googleRedirectUri;

    private String sduAiApiKey;
    private String sduAiApiUrl;

    private String securityKey;
    private String testUser;
    private String testUserPassword;
}
