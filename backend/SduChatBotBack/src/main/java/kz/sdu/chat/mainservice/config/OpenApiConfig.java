package kz.sdu.chat.mainservice.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeIn;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.security.SecurityScheme;
import io.swagger.v3.oas.annotations.servers.Server;
import io.swagger.v3.oas.models.media.StringSchema;
import io.swagger.v3.oas.models.parameters.Parameter;
import org.springdoc.core.customizers.GlobalOpenApiCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
@OpenAPIDefinition(
        info = @Info(
                contact = @Contact(
                        name = "qqanly",
                        email = "akhan.dulatbay@gmail.com",
                        url = ""
                ),
                description = "OpenApi documentation for SDU AI CHAT",
                title = "OpenApi specification - SDU AI CHAT",
                version = "1.0",
                license = @License(
                        name = "Licence name",
                        url = ""
                ),
                termsOfService = "Terms of service"
        ),
        servers = {
                @Server(
                        description = "PROD ENV",
                        url = "https://chat-back.sdu.edu.kz/api"
                ),
                @Server(
                        description = "Local ENV",
                        url = "http://localhost:8080/api")
        },
        security = {
                @SecurityRequirement(
                        name = "bearerAuth"
                )
        }
)
@SecurityScheme(
        name = "bearerAuth",
        description = "JWT auth description",
        scheme = "bearer",
        type = SecuritySchemeType.HTTP,
        bearerFormat = "JWT",
        in = SecuritySchemeIn.HEADER
)
public class OpenApiConfig {
    @Bean
    public GlobalOpenApiCustomizer customGlobalHeader() {
        return openApi -> openApi.getPaths().values().forEach(pathItem -> pathItem.readOperations().forEach(operation -> {
            Parameter acceptLanguageHeader = new Parameter()
                    .in("header")
                    .name("Accept-Language")
                    .description("Supported locales: KZ, RU, TR, DE, CN, ES, FR, US")
                    .schema(new StringSchema()._enum(List.of("KZ", "RU", "TR", "DE", "CN", "ES", "FR", "US"))._default("RU"))
                    .required(false);

            operation.addParametersItem(acceptLanguageHeader);
        }));
    }
}
