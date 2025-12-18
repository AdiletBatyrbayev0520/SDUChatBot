package kz.sdu.chat.mainservice.rest.controllers;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import kz.sdu.chat.mainservice.rest.dto.request.LoginDevRequest;
import kz.sdu.chat.mainservice.rest.dto.response.LoginResponse;
import kz.sdu.chat.mainservice.services.AuthService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping("/auth")
@Tag(name = "Authentication", description = "OAuth2 login, developer login and session termination endpoints")
public class AuthController {
    private final AuthService authService;

    @GetMapping("/login")
    @Operation(
            summary = "Complete Google OAuth login",
            description = "Exchanges the Google authorization code received from the frontend redirect for SDU Chat access and refresh JWT tokens.",
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Tokens successfully generated",
                            content = @Content(schema = @Schema(implementation = LoginResponse.class))),
                    @ApiResponse(
                            responseCode = "400",
                            description = "Invalid or expired authorization code"),
                    @ApiResponse(
                            responseCode = "500",
                            description = "Unexpected error while contacting Google OAuth or issuing JWT tokens")
            }
    )
    public LoginResponse grantCode(
            @Parameter(description = "Authorization code returned by Google OAuth redirect", required = true)
            @RequestParam("code") String code,
            @Parameter(description = "Granted scopes that came with the authorization code", required = true)
            @RequestParam("scope") String scope,
            @Parameter(description = "Google user identifier selected during multi-account consent", required = true)
            @RequestParam("authuser") String authUser,
            @Parameter(description = "Prompt metadata returned by Google OAuth", required = true)
            @RequestParam("prompt") String prompt) {
        log.info("Processing grant code: {}, scope: {}, authUser: {}, prompt: {}", code, scope, authUser, prompt);
        return authService.processGrantCode(code);
    }

    @PostMapping("/login-dev")
    @Operation(
            summary = "Authenticate developer without Google OAuth",
            description = "Performs a direct login for trusted developers using email, password and one more security key. Use only in non-production environments.",
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    required = true,
                    description = "Developer credentials, including the out-of-band security key",
                    content = @Content(schema = @Schema(implementation = LoginDevRequest.class))),
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Developer successfully authenticated",
                            content = @Content(schema = @Schema(implementation = LoginResponse.class))),
                    @ApiResponse(
                            responseCode = "401",
                            description = "Invalid developer credentials or security key")
            }
    )
    public LoginResponse loginDev(@RequestBody LoginDevRequest loginDevRequest) {
        return authService.loginDev(loginDevRequest);
    }

    @PostMapping("/logout")
    @Operation(
            summary = "Terminate current session",
            description = "Revokes refresh tokens and clears cookies for the active user. Requires a valid bearer token.",
            security = @SecurityRequirement(name = "bearerAuth"),
            responses = {
                    @ApiResponse(
                            responseCode = "204",
                            description = "Logout successful, no response body"),
                    @ApiResponse(
                            responseCode = "401",
                            description = "Missing or invalid bearer token")
            }
    )
    public ResponseEntity<Void> logout(HttpServletRequest request, HttpServletResponse response) {
        authService.logout(request, response);
        return ResponseEntity.noContent().build();
    }
}
