package kz.sdu.chat.mainservice.rest.dto.request;

import lombok.Data;

@Data
public class LoginDevRequest {
    private String email;
    private String password;
    private String securityKey;
}
