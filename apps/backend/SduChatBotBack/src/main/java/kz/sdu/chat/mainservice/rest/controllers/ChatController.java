package kz.sdu.chat.mainservice.rest.controllers;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import kz.sdu.chat.mainservice.constants.Utils;
import kz.sdu.chat.mainservice.rest.dto.request.ChatCreateRequest;
import kz.sdu.chat.mainservice.rest.dto.request.MessageCreateRequest;
import kz.sdu.chat.mainservice.rest.dto.response.ChatResponse;
import kz.sdu.chat.mainservice.rest.dto.base.PaginatedResponse;
import kz.sdu.chat.mainservice.rest.dto.base.PaginationParams;
import kz.sdu.chat.mainservice.rest.dto.response.MessageResponse;
import kz.sdu.chat.mainservice.rest.dto.response.SendMessageResponse;
import kz.sdu.chat.mainservice.services.ChatService;
import kz.sdu.chat.mainservice.services.MessageService;
import kz.sdu.chat.mainservice.services.MessageTokenService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springdoc.core.annotations.ParameterObject;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@Slf4j
@RequiredArgsConstructor
@RequestMapping("/chats")
@RestController
@PreAuthorize("isAuthenticated()")
@Tag(name = "Chats & Messages", description = "Chat lifecycle management, message history and AI message sending")
@SecurityRequirement(name = "bearerAuth")
public class ChatController {
    private final ChatService chatService;
    private final MessageService messageService;
    private final MessageTokenService messageTokenService;

    @GetMapping("/connected")
    @Operation(
            summary = "Check external model connection",
            description = "Returns true when the underlying SDU AI connector reports an active session and false otherwise.",
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Connection probe result",
                            content = @Content(schema = @Schema(implementation = Boolean.class)))
            }
    )
    public ResponseEntity<Boolean> getConnectedChats() {
        return ResponseEntity.ok(Optional.ofNullable(chatService.getConnectionStatus()).isPresent());
    }

    @GetMapping
    @Operation(
            summary = "List chats for the current user",
            description = "Returns a paginated list of chats ordered by creation date. Page index starts from 0.",
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Page of chats",
                            content = @Content(schema = @Schema(implementation = PaginatedResponse.class)))
            }
    )
    public ResponseEntity<PaginatedResponse<ChatResponse>> getChat(@ParameterObject @ModelAttribute PaginationParams paginationParams) {
        var user = Utils.getCurrentUser();
        var chats = chatService.getChats(user, paginationParams);
        return ResponseEntity.ok(new PaginatedResponse<>(chats));
    }

    @GetMapping("/{chatId}")
    @Operation(
            summary = "Fetch chat metadata",
            description = "Loads a single chat that belongs to the current user.",
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Chat was found",
                            content = @Content(schema = @Schema(implementation = ChatResponse.class))),
                    @ApiResponse(
                            responseCode = "404",
                            description = "Chat does not belong to the user or is missing")
            }
    )
    public ResponseEntity<ChatResponse> getChatById(
            @Parameter(description = "Unique identifier of the chat", required = true)
            @PathVariable long chatId) {
        var user = Utils.getCurrentUser();
        log.info("Fetching chat with ID: {}", chatId);
        var chatResponse = chatService.getChatById(chatId, user);
        return ResponseEntity.ok(chatResponse);
    }

    @PostMapping
    @Operation(
            summary = "Create an empty chat",
            description = "Registers a new chat container for the current user without sending an initial prompt.",
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    required = true,
                    description = "Chat title or subject",
                    content = @Content(schema = @Schema(implementation = ChatCreateRequest.class))),
            responses = {
                    @ApiResponse(
                            responseCode = "201",
                            description = "Chat created successfully, no response body"),
                    @ApiResponse(
                            responseCode = "400",
                            description = "Validation error in the request payload")
            }
    )
    public ResponseEntity<Void> createChat(@RequestBody ChatCreateRequest chatCreateRequest) {
        var user = Utils.getCurrentUser();

        log.info("Creating chat with title: {}", chatCreateRequest.getTitle());
        chatService.createChat(chatCreateRequest, user);
        return ResponseEntity.status(201).build();
    }

    @DeleteMapping("/{chatId}")
    @Operation(
            summary = "Delete chat with all messages",
            description = "Removes the chat and its history if it belongs to the current user.",
            responses = {
                    @ApiResponse(
                            responseCode = "204",
                            description = "Chat deleted"),
                    @ApiResponse(
                            responseCode = "404",
                            description = "Chat not found for the user")
            }
    )
    public ResponseEntity<Void> deleteChat(
            @Parameter(description = "Identifier of the chat to delete", required = true)
            @PathVariable long chatId) {
        var user = Utils.getCurrentUser();
        log.info("Deleting chat with ID: {}", chatId);
        chatService.deleteChat(chatId, user);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/{chatId}/messages")
    @Operation(
            summary = "List chat messages",
            description = "Returns the chronological message history for the chat, including both user and assistant turns.",
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Page of messages",
                            content = @Content(schema = @Schema(implementation = PaginatedResponse.class))),
                    @ApiResponse(
                            responseCode = "404",
                            description = "Chat not found for the current user")
            }
    )
    public ResponseEntity<PaginatedResponse<MessageResponse>> getMessages(
            @Parameter(description = "Identifier of the chat", required = true)
            @PathVariable long chatId,
            @ParameterObject @ModelAttribute PaginationParams paginationParams) {
        log.info("Fetching messages for chat with ID: {}", chatId);
        var user = Utils.getCurrentUser();
        var messages = messageService.getMessagesForChat(chatId, user, paginationParams);
        return ResponseEntity.ok(new PaginatedResponse<>(messages));
    }

    @PostMapping("/{chatId}/messages")
    @Operation(
            summary = "Send message to an existing chat",
            description = "Appends a user message to the chat and streams the SDU AI assistant reply once ready.",
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    required = true,
                    description = "Plain text user prompt",
                    content = @Content(schema = @Schema(implementation = MessageCreateRequest.class))),
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Assistant response",
                            content = @Content(schema = @Schema(implementation = SendMessageResponse.class))),
                    @ApiResponse(
                            responseCode = "404",
                            description = "Chat not found for the current user")
            }
    )
    public ResponseEntity<SendMessageResponse> sendMessage(
            @Parameter(description = "Identifier of the chat that should receive the message", required = true)
            @PathVariable long chatId,
            @RequestBody MessageCreateRequest messageCreateRequest) {
        var user = Utils.getCurrentUser();
        log.info("Sending message to chat with ID: {}", chatId);
        return ResponseEntity.ok(messageService.sendMessage(chatId, messageCreateRequest, user));
    }

    @PostMapping("/send-message")
    @Operation(
            summary = "Create chat and send message in one call",
            description = "Creates a new chat for the user, stores the first user message and returns the AI reply.",
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    required = true,
                    description = "Plain text user prompt",
                    content = @Content(schema = @Schema(implementation = MessageCreateRequest.class))),
            responses = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "Assistant response with chat metadata",
                            content = @Content(schema = @Schema(implementation = SendMessageResponse.class)))
            }
    )
    public ResponseEntity<SendMessageResponse> sendMessageToChat(@RequestBody MessageCreateRequest messageCreateRequest) {
        var user = Utils.getCurrentUser();
        log.info("Sending message to chat with content: {}", messageCreateRequest.getContent());
        return ResponseEntity.ok(messageService.createChatAndSendMessage(messageCreateRequest, user));
    }
}

