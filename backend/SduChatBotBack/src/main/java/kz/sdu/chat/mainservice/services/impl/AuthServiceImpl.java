package kz.sdu.chat.mainservice.services.impl;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import kz.sdu.chat.mainservice.config.ApplicationProperties;
import kz.sdu.chat.mainservice.entities.Role;
import kz.sdu.chat.mainservice.entities.Token;
import kz.sdu.chat.mainservice.entities.User;
import kz.sdu.chat.mainservice.feign.google.GoogleAPI;
import kz.sdu.chat.mainservice.repositories.TokenRepository;
import kz.sdu.chat.mainservice.repositories.UserRepository;
import kz.sdu.chat.mainservice.rest.dto.request.LoginDevRequest;
import kz.sdu.chat.mainservice.rest.dto.response.LoginResponse;
import kz.sdu.chat.mainservice.security.JwtService;
import kz.sdu.chat.mainservice.services.AuthService;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpHeaders;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.nio.file.AccessDeniedException;
import java.time.LocalDateTime;

import static kz.sdu.chat.mainservice.constants.ValueConstants.ZONE_ID;


@Slf4j
@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {
    private final GoogleAPI googleAPI;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final TokenRepository tokenRepository;
    private final ApplicationProperties applicationProperties;

    @Override
    public LoginResponse processGrantCode(String code) {
        String accessToken = googleAPI.getOauthAccessTokenGoogle(code).getAccessToken();
        User googleUser = googleAPI.fetchGoogleUserProfile(accessToken);
        log.info("Google user info: {}", googleUser.getEmail());
        User user = userRepository.findByEmail(googleUser.getEmail())
                .orElseGet(() -> registerUser(googleUser.getFirstName(), googleUser.getLastName(), googleUser.getEmail(), passwordEncoder.encode(googleUser.getEmail())));


        String refreshToken = jwtService.generateRefreshToken(user);
        String token = jwtService.generateToken(user);
        saveUserToken(user, refreshToken);

        return LoginResponse.builder()
                .accessToken(token)
                .refreshToken(refreshToken)
                .build();
    }

    @Override
    public void logout(HttpServletRequest request, HttpServletResponse response) {
        String refreshToken = getRefreshTokenFromHeader(request);
        String username = jwtService.extractUsername(refreshToken);

        if (username == null) {
            throw new IllegalArgumentException("Invalid token");
        }

        revokeCurrentToken(refreshToken);

        response.setStatus(HttpServletResponse.SC_NO_CONTENT);
    }

    private void validateSecurityKey(String securityKey) {
        if(!applicationProperties.getSecurityKey().equals(securityKey)) {
            throw new IllegalArgumentException("Invalid security key");
        }
    }

    @Override
    public LoginResponse loginDev(LoginDevRequest loginDevRequest) {
        validateSecurityKey(loginDevRequest.getSecurityKey());

        User foundUser = userRepository.findByEmail(loginDevRequest.getEmail())
                .orElseThrow(() -> new IllegalArgumentException("User not found"));

        if (!passwordEncoder.matches(loginDevRequest.getPassword(), foundUser.getPassword())) {
            throw new IllegalArgumentException("Invalid credentials");
        }

        String refreshToken = jwtService.generateRefreshToken(foundUser);
        String token = jwtService.generateToken(foundUser);
        saveUserToken(foundUser, refreshToken);

        return LoginResponse.builder()
                .accessToken(token)
                .refreshToken(refreshToken)
                .build();
    }

    private void revokeCurrentToken(String refreshToken) {
        var token = tokenRepository.findByToken(refreshToken)
                .orElseThrow(() -> new IllegalArgumentException("Invalid token"));

        token.setExpired(true);
        token.setRevoked(true);
        tokenRepository.save(token);
    }

    @SneakyThrows
    private String getRefreshTokenFromHeader(HttpServletRequest request) {
        String authorizationHeader = request.getHeader(HttpHeaders.AUTHORIZATION);
        if (authorizationHeader != null && authorizationHeader.startsWith("Bearer ")) {
            return authorizationHeader.substring(7);
        }

        throw new AccessDeniedException("forbidden");
    }

    private void saveUserToken(User user, String jwtToken) {
        LocalDateTime expiredAt = LocalDateTime.now(ZONE_ID).plusSeconds(jwtService.getRefreshExpiration() / 1000);

        var token = Token.builder()
                .user(user)
                .token(jwtToken)
                .expirationTime(expiredAt)
                .build();
        tokenRepository.save(token);
    }

    private User registerUser(String firstName, String lastName, String email, String password) {
        User user = new User();
        user.setEnabled(true);
        user.setRole(Role.USER);
        user.setFirstName(firstName);
        user.setLastName(lastName);
        user.setEmail(email);
        user.setPassword(passwordEncoder.encode(password));

        user = userRepository.save(user);

        return user;
    }
}
