package kz.sdu.chat.mainservice.config;

import kz.sdu.chat.mainservice.constants.Utils;
import kz.sdu.chat.mainservice.entities.User;
import org.springframework.data.domain.AuditorAware;
import org.springframework.stereotype.Component;

import java.util.Optional;

@Component
public class AuditorAwareImpl implements AuditorAware<String> {

    @Override
    public Optional<String> getCurrentAuditor() {
        User currentUser = Utils.getCurrentUser();
        return Optional.of(currentUser == null ? "anonymous" : currentUser.getEmail());
    }
}

