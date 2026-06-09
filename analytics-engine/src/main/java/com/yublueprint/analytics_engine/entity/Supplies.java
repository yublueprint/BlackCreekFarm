package com.yublueprint.analytics_engine.entity;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "app_supplies")
@Data
public class Supplies {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String category;
    private Double quantity;
    private String unit;

    @Column(name = "minimum_required")
    private Double minimumRequired;
}
