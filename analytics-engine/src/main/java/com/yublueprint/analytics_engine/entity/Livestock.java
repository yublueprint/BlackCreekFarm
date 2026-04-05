package com.yublueprint.analytics_engine.entity;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "app_livestock")
@Data
public class Livestock {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String breed;
    private Integer age;
    private Double weight;

    @Column(name = "health_status")
    private String healthStatus;

    @Column(name = "purchase_price")
    private Double purchasePrice;

    @Column(name = "current_value")
    private Double currentValue;

    @Column(name = "next_vaccination_date")
    private java.time.LocalDate nextVaccinationDate;

    private String notes;
}
