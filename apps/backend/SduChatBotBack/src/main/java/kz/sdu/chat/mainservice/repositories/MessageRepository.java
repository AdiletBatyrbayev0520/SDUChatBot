package kz.sdu.chat.mainservice.repositories;

import kz.sdu.chat.mainservice.entities.Message;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MessageRepository extends JpaRepository<Message, Long> {
    Page<Message> findAllByChatId(long chatId, Pageable pageable);
}
