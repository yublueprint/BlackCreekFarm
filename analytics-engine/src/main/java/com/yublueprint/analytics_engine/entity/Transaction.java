package com.yublueprint.analytics_engine.entity;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDate;

@Entity
@Table(name = "app_transaction")
@Data
public class Transaction {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "item_type")
    private String itemType;

    @Column(name = "item_id")
    private Long itemId;

    @Column(name = "transaction_type")
    private String transactionType;

    private Integer quantity;

    private LocalDate date;
}
