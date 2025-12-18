package kz.sdu.chat.mainservice.entities;

import jakarta.persistence.*;
import kz.sdu.chat.mainservice.entities.base.BaseEntity;
import kz.sdu.chat.mainservice.rest.dto.response.UsageMetadataResponse;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.Type;
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
public class Message extends BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(columnDefinition = "TEXT")
    private String content;
    private boolean isUser;

    @JdbcTypeCode(SqlTypes.JSON)
    private List<Integer> versions = List.of(1);

    @JdbcTypeCode(SqlTypes.JSON)
    private List<String> sources = new ArrayList<>();

    private Double costUsd;

    @ManyToOne
    @JoinColumn(name = "chat_id")
    private Chat chat;
}
