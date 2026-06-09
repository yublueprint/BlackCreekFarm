package com.yublueprint.analytics_engine.repository;

import com.yublueprint.analytics_engine.entity.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    List<Transaction> findByItemTypeAndDateAfter(String itemType, LocalDate date);
}
