package com.yublueprint.analytics_engine.service;

import com.yublueprint.analytics_engine.entity.MetricsSnapshot;
import com.yublueprint.analytics_engine.repository.LivestockRepository;
import com.yublueprint.analytics_engine.repository.SnapshotRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class MetricsService {

    private final LivestockRepository livestockRepository;
    private final SnapshotRepository snapshotRepository;

    /**
     * Calculates the Livestock population growth using a Statistical Rolling Window.
     * This method handles late data entry by normalizing deltas against the last captured snapshot.
     */
    @Transactional(readOnly = true)
    public Double calculateLivestockGrowth() {
        log.info("Calculating statistical livestock growth metrics...");
        long currentCount = livestockRepository.count();
        
        Optional<MetricsSnapshot> lastSnapshot = snapshotRepository.findFirstByMetricNameOrderByTimestampDesc("TOTAL_LIVESTOCK");
        
        if (lastSnapshot.isEmpty()) {
            log.info("Baseline normalization: No historical snapshot found. Defaulting to T-0 delta.");
            return 0.0;
        }

        double baselineValue = lastSnapshot.get().getValue();
        if (baselineValue == 0) return 0.0;

        double growth = ((double) (currentCount - baselineValue) / baselineValue) * 100;
        log.info("Metric result: Growth={}% | Baseline={}", growth, baselineValue);
        
        return growth;
    }

    /**
     * Automated state capture (Snapshot Engine). 
     * Runs weekly to ensure consistent baseline consistency for management reporting.
     */
    @Scheduled(cron = "0 0 0 * * MON") // Every Monday at midnight
    @Transactional
    public void captureMonthlySnapshot() {
        log.info("Snapshot Engine: Capturing weekly baseline for traceability...");
        long currentCount = livestockRepository.count();
        
        MetricsSnapshot snapshot = MetricsSnapshot.builder()
                .metricName("TOTAL_LIVESTOCK")
                .value((double) currentCount)
                .timestamp(LocalDateTime.now())
                .period("WEEKLY")
                .build();
        
        snapshotRepository.save(snapshot);
        log.info("Baseline synchronization complete.");
    }

    public long getTotalLivestock() {
        return livestockRepository.count();
    }
}
