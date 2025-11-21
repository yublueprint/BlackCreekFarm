package com.blackcreekfarm.analyticsconsumer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import jakarta.annotation.PostConstruct;
import java.time.LocalDateTime;

@SpringBootApplication
public class AnalyticsConsumerApplication {

    public static void main(String[] args) {
        SpringApplication.run(AnalyticsConsumerApplication.class, args);
    }

    @PostConstruct
    public void onStartup() {
        System.out.println("===============================================");
        System.out.println(" BlackCreekFarm Analytics Consumer Started");
        System.out.println(" Environment: " + System.getProperty("spring.profiles.active", "default"));
        System.out.println(" Startup Time: " + LocalDateTime.now());
        System.out.println(" Waiting for analytics events in Redis...");
        System.out.println("=====================================");
    }
}
