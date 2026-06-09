package com.yublueprint.analytics_engine.repository;

import com.yublueprint.analytics_engine.entity.Livestock;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LivestockRepository extends JpaRepository<Livestock, Long> {
}
