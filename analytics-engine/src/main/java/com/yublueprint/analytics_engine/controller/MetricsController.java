package com.yublueprint.analytics_engine.controller;

import com.yublueprint.analytics_engine.service.MetricsService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/metrics")
@RequiredArgsConstructor
public class MetricsController {

    private final MetricsService metricsService;

    @GetMapping("/livestock/growth")
    public Map<String, Object> getLivestockGrowth() {
        Map<String, Object> metrics = new HashMap<>();
        metrics.put("total", metricsService.getTotalLivestock());
        metrics.put("growth_percentage", metricsService.calculateLivestockGrowth());
        return metrics;
    }
}
