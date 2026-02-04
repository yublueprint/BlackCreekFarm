package com.blackcreekfarm.analyticsconsumer.consumer;

import org.springframework.data.redis.connection.stream.Consumer;
import org.springframework.data.redis.connection.stream.MapRecord;
import org.springframework.data.redis.connection.stream.ReadOffset;
import org.springframework.data.redis.connection.stream.StreamOffset;
import org.springframework.data.redis.connection.stream.StreamReadOptions;
import org.springframework.data.redis.core.StringRedisTemplate;

import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class EventConsumer {

    private final StringRedisTemplate redis;
    private final String stream;
    private final String group;
    private final String consumerName;

    public EventConsumer(
            StringRedisTemplate redis,
            String stream,
            String group,
            String consumerName
    ) {
        this.redis = redis;
        this.stream = stream;
        this.group = group;
        this.consumerName = consumerName;
    }

    public void startPolling() {

        System.out.println("🚀 Starting event polling for stream: " + stream);

        while (true) {

            try {
                List<MapRecord<String, Object, Object>> records =
                        redis.opsForStream().read(
                                Consumer.from(group, consumerName),
                                StreamReadOptions.empty()
                                        .count(5)
                                        .block(Duration.ofMillis(500)),
                                StreamOffset.create(stream, ReadOffset.lastConsumed())
                        );

                if (records != null && !records.isEmpty()) {

                    for (MapRecord<String, Object, Object> record : records) {

                        Map<String, String> event = new HashMap<>();
                        for (Map.Entry<Object, Object> entry : record.getValue().entrySet()) {
                            event.put(
                                    entry.getKey().toString(),
                                    entry.getValue().toString()
                            );
                        }

                        System.out.println("🔥 EVENT RECEIVED");
                        System.out.println("🆔 ID: " + record.getId());
                        System.out.println("📦 DATA: " + event);
                        System.out.println("--------------------------------");

                        redis.opsForStream().acknowledge(stream, group, record.getId());
                    }
                }

                Thread.sleep(1000); // manual interval

            } catch (Exception e) {
                System.out.println("❌ Error reading stream: " + e.getMessage());
            }
        }
    }
}
