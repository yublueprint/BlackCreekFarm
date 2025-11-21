package com.blackcreekfarm.analyticsconsumer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class AnalyticsConsumerApplication {

    public static void main(String[] args) {
        SpringApplication.run(AnalyticsConsumerApplication.class, args);
    }
}
