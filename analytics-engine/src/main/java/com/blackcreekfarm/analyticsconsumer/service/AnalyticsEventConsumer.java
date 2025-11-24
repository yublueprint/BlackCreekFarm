package com.blackcreekfarm.analyticsconsumer.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class AnalyticsEventConsumer {

    @Autowired
    private StringRedisTemplate redis;

    @Scheduled(fixedRate = 500)
    public void consumeEvents() {
        try {
            String event = redis.opsForList().rightPop("analytics_events");
            if (event != null) {
                log.info("📥 RECEIVED EVENT → {}", event);
            }
        } catch (Exception e) {
            log.error("❌ ERROR reading Redis: {}", e.getMessage());
        }
    }
}
