package kz.sdu.chat.mainservice.services;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import kz.sdu.chat.mainservice.rest.dto.request.LoginDevRequest;
import kz.sdu.chat.mainservice.rest.dto.response.LoginResponse;

public interface AuthService {
    LoginResponse processGrantCode(String code);

    void logout(HttpServletRequest request, HttpServletResponse response);

    LoginResponse loginDev(LoginDevRequest loginDevRequest);
}
