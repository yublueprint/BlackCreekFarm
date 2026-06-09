package com.yublueprint.analytics_engine.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "metrics_snapshots")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MetricsSnapshot {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String metricName;

    @Column(nullable = false)
    private Double value;

    @Column(nullable = false)
    private LocalDateTime timestamp;

    @Column(nullable = false)
    private String period; // e.g., "MONTHLY", "DAILY"
}
