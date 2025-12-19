package kz.sdu.chat.mainservice;

import kz.sdu.chat.mainservice.config.ApplicationProperties;
import kz.sdu.chat.mainservice.entities.Role;
import kz.sdu.chat.mainservice.entities.User;
import kz.sdu.chat.mainservice.repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.security.crypto.password.PasswordEncoder;

@Slf4j
@SpringBootApplication
@RequiredArgsConstructor
public class MainServiceApplication implements CommandLineRunner {
    private final ApplicationProperties applicationProperties;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    public static void main(String[] args) {
        SpringApplication.run(MainServiceApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        log.info("Application command line started with");

        var foundUser = userRepository.findByEmail(applicationProperties.getTestUser());

        if(foundUser.isEmpty()) {
            log.info("Creating test user");
            User userToCreate = new User();
            userToCreate.setEnabled(true);
            userToCreate.setRole(Role.USER);
            userToCreate.setFirstName("test_firstName");
            userToCreate.setLastName("test_lastName");
            userToCreate.setEmail(applicationProperties.getTestUser());
            userToCreate.setPassword(passwordEncoder.encode(applicationProperties.getTestUserPassword()));
            userRepository.save(userToCreate);
            log.info("Test user created successfully");
        }

        log.info("Application command line finished");
    }
}
