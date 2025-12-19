package kz.sdu.chat.mainservice.entities;

import jakarta.persistence.*;
import kz.sdu.chat.mainservice.entities.base.BaseEntity;
import lombok.*;
import org.hibernate.annotations.GenericGenerator;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.UuidGenerator;
import org.hibernate.type.SqlTypes;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Chat extends BaseEntity {
    @Id
    @GeneratedValue(generator = "uuid")
    @Column(updatable = false, nullable = false)
    private long id;

    @Column(unique = true, nullable = false)
    @UuidGenerator
    private String uniqueUUID;

    @Column(columnDefinition = "TEXT")
    private String title;

    @ManyToOne
    @JoinColumn(name = "owner_id")
    private User owner;

    private int maxVersion = 1;

    @OneToMany(mappedBy = "chat", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    private List<Message> messages = new ArrayList<>();
}
