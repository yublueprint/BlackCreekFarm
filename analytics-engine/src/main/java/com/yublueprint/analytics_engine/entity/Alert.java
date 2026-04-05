package com.yublueprint.analytics_engine.entity;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

@Entity
@Table(name = "app_alert")
@Data
public class Alert {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    private String message;
    private String severity;
    private LocalDateTime timestamp;

    @Column(name = "is_read")
    private boolean isRead;

    @Column(name = "item_type")
    private String itemType;

    @Column(name = "item_id")
    private Long itemId;
}
