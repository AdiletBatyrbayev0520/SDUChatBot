package kz.sdu.chat.mainservice.entities;

import jakarta.persistence.*;
import kz.sdu.chat.mainservice.entities.base.BaseEntity;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Token extends BaseEntity {
    @Id
    private String token;
    private LocalDateTime expirationTime;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    private Boolean revoked = false;
    private Boolean expired = false;
}
