package com.blackcreekfarm.analyticsconsumer.config;

import org.springframework.data.redis.connection.stream.ReadOffset;
import org.springframework.data.redis.connection.stream.StreamRecords;
import org.springframework.data.redis.core.StringRedisTemplate;

import java.util.HashMap;
import java.util.Map;

public class RedisStreamInitializer {

    private final StringRedisTemplate redis;
    private final String streamName;
    private final String groupName;

    public RedisStreamInitializer(
            StringRedisTemplate redis,
            String streamName,
            String groupName
    ) {
        this.redis = redis;
        this.streamName = streamName;
        this.groupName = groupName;
    }

    public void init() {

        Boolean exists = redis.hasKey(streamName);

        if (exists == null || !exists) {
            System.out.println("⚙️ Creating stream: " + streamName);

            Map<String, String> initData = new HashMap<>();
            initData.put("init", "true");

            redis.opsForStream().add(
                    StreamRecords.mapBacked(initData).withStreamKey(streamName)
            );
        }

        try {
            redis.opsForStream().createGroup(
                    streamName,
                    ReadOffset.from("0-0"),
                    groupName
            );

            System.out.println("✔ Consumer group created: " + groupName);

        } catch (Exception e) {
            System.out.println("ℹ Consumer group already exists: " + groupName);
        }
    }
}
