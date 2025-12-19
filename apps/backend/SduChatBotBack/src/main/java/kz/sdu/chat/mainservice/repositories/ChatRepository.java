package kz.sdu.chat.mainservice.repositories;

import kz.sdu.chat.mainservice.entities.Chat;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface ChatRepository extends JpaRepository<Chat, Long> {
    @Query("SELECT c FROM Chat c WHERE c.owner.id = :userId AND c.deleted = false ORDER BY c.createdDate DESC")
    Page<Chat> findAllByOwnerId(Long userId, Pageable pageable);
}
