package com.yublueprint.analytics_engine.repository;

import com.yublueprint.analytics_engine.entity.MetricsSnapshot;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface SnapshotRepository extends JpaRepository<MetricsSnapshot, Long> {
    Optional<MetricsSnapshot> findFirstByMetricNameOrderByTimestampDesc(String metricName);
}
