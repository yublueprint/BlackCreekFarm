package com.yublueprint.analytics_engine.repository;

import com.yublueprint.analytics_engine.entity.Alert;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AlertRepository extends JpaRepository<Alert, Long> {
}
