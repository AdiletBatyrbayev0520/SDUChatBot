package kz.sdu.chat.mainservice.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.NonNull;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

@Slf4j
@Component
public class CustomCorsFilter extends OncePerRequestFilter {

    private final List<String> allowedOrigins = Arrays.asList(
        "http://localhost:3000", 
        "http://localhost:3001", 
        "http://192.168.0.37:3000", 
        "http://localhost:5173",
        "https://main.d36vvvf4ztyfx9.amplifyapp.com",
        "https://18.244.146.111:443",
        "http://localhost",
        "http://3.120.37.156",
        "https://chat.sdu.edu.kz",
        "https://dev.dsfyww8pm8b26.amplifyapp.com",
        "http://3.73.120.186:5173",
        "https://chat-back.sdu.edu.kz"
    );

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    @NonNull HttpServletResponse response,
                                    @NonNull FilterChain filterChain) throws ServletException, IOException {

        String origin = request.getHeader("Origin");

        if (allowedOrigins.contains(origin)) {
            response.setHeader("Access-Control-Allow-Origin", origin);
        }
        response.setHeader("Access-Control-Allow-Credentials", "true");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH");
        response.setHeader("Access-Control-Max-Age", "3600");
        response.setHeader("Access-Control-Allow-Headers", "authorization, content-type, accept-language");


        if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
            response.setStatus(HttpServletResponse.SC_OK);
            return;
        }

        filterChain.doFilter(request, response);
    }
}

