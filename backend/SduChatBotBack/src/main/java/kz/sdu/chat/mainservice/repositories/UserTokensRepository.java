package kz.sdu.chat.mainservice.repositories;

import kz.sdu.chat.mainservice.entities.UserTokens;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserTokensRepository extends JpaRepository<UserTokens, Long> {
    UserTokens findAllByUserId(long userId);
}
