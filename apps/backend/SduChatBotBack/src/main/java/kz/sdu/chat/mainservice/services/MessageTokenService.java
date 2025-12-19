package kz.sdu.chat.mainservice.services;

import kz.sdu.chat.mainservice.entities.User;
import org.springframework.scheduling.annotation.Scheduled;

public interface MessageTokenService {
    void checkMessageToken(User user);

    void addtokenToUser(User user, Double cost);

    void createUserToken(User user);

    void checkForDateUserToken();
}
