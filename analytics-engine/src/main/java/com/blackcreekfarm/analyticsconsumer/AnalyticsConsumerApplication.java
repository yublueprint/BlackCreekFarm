package com.blackcreekfarm.analyticsconsumer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.data.redis.core.StringRedisTemplate;

import com.blackcreekfarm.analyticsconsumer.config.RedisStreamInitializer;
import com.blackcreekfarm.analyticsconsumer.consumer.EventConsumer;

@SpringBootApplication
public class AnalyticsConsumerApplication {

    public static void main(String[] args) {

        ConfigurableApplicationContext ctx =
                SpringApplication.run(AnalyticsConsumerApplication.class, args);

        StringRedisTemplate redis = ctx.getBean(StringRedisTemplate.class);

        RedisStreamInitializer initializer =
                new RedisStreamInitializer(redis, "farm-events", "analytics-group");

        initializer.init();

        EventConsumer consumer =
                new EventConsumer(redis, "farm-events", "analytics-group", "consumer-1");

        consumer.startPolling();
    }
}
