package com.yublueprint.analytics_engine.repository;

import com.yublueprint.analytics_engine.entity.Supplies;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SuppliesRepository extends JpaRepository<Supplies, Long> {
    List<Supplies> findByQuantityLessThan(Double quantity);
}
