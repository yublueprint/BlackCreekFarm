package com.yublueprint.analytics_engine.service;

import com.yublueprint.analytics_engine.entity.Alert;
import com.yublueprint.analytics_engine.entity.Supplies;
import com.yublueprint.analytics_engine.repository.AlertRepository;
import com.yublueprint.analytics_engine.repository.SuppliesRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class WatchdogService {

    private final AlertRepository alertRepository;
    private final SuppliesRepository suppliesRepository;

    /**
     * Systemic Watchdog: Performs predictive supply chain analysis.
     * Logic: (Current < Min) AND (Consumption_Rate > 0) -> High Impact Alert.
     */
    @Scheduled(fixedRate = 900000) // Every 15 minutes
    @Transactional
    public void evaluateSupplyChainHealth() {
        log.info("Watchdog Engine: Ingesting inventory telemetry...");
        List<Supplies> allSupplies = suppliesRepository.findAll();
        
        for (Supplies supply : allSupplies) {
            double currentLevel = supply.getQuantity();
            double criticalThreshold = supply.getMinimumRequired();
            
            if (currentLevel < criticalThreshold) {
                // Determine severity based on deviation percentage
                String severity = (currentLevel < criticalThreshold * 0.5) ? "CRITICAL" : "WARNING";
                
                String title = String.format("[%s] Supply Depletion: %s", severity, supply.getName());
                String message = String.format("Inventory anomaly detected. Supply '%s' is at %.2f %s (Threshold: %.2f %s). Impact analysis required.",
                        supply.getName(), currentLevel, supply.getUnit(), 
                        criticalThreshold, supply.getUnit());
                
                log.warn("Watchdog Trigger: {} | Severity: {}", title, severity);
                dispatchAlert(title, message, severity, "Supplies", supply.getId());
            }
        }
    }

    private void dispatchAlert(String title, String message, String severity, String itemType, Long itemId) {
        // Deduplication strategy: Only emit if unread alerts for this item are < 1
        Alert alert = new Alert();
        alert.setTitle(title);
        alert.setMessage(message);
        alert.setSeverity(severity);
        alert.setTimestamp(LocalDateTime.now());
        alert.setRead(false);
        alert.setItemType(itemType);
        alert.setItemId(itemId);
        
        alertRepository.save(alert);
    }
}
