# Analytics Consumer - Quick Setup

## Prerequisites
- Java 21 ([Download](https://adoptium.net/temurin/releases/))
- IntelliJ IDEA ([Download](https://www.jetbrains.com/idea/download/))
- Docker Desktop

## Setup Steps

### 1. Install Java 21
Download and run installer. **Important:** Enable "Set JAVA_HOME" and "Add to PATH" options.

Verify:
```bash
java -version
```

### 2. Install IntelliJ IDEA
Download Community Edition, install, and add Lombok plugin on first launch.

### 3. Open Project
1. Open IntelliJ → **Open** → Select `analytics-engine/` folder
2. Wait for indexing to complete

### 4. Configure Java SDK
1. **File** → **Project Structure** (`Ctrl+Alt+Shift+S`)
2. **Project** → Set SDK to **21**
3. Set language level to **21**
4. **Apply** → **OK**

### 5. Enable Annotation Processing
1. **File** → **Settings** → Search "annotation"
2. **Compiler** → **Annotation Processors**
3. Check **Enable annotation processing**
4. **Apply** → **OK**

### 6. Reload Maven
Right sidebar → **Maven** tab → Click **🔄 Reload All Maven Projects**

### 7. Start Redis
```bash
docker-compose up -d
```

**Test Redis connection:**
```bash
redis-cli ping
# Should return "PONG"
```

### 8. Run Application
Click the **▶️** button next to `AnalyticsConsumerApplication` class or `main` method.

Expected output:
```
Started AnalyticsConsumerApplication in X seconds
Polling Redis queue: analytics_events
```

## Quick Test

**Trigger analytics manually:**
```bash
redis-cli lpush analytics_events '{ "event": "Hello, Black Creek Farm!" }'
```

Check IntelliJ console for "Received event" message.

## Daily Commands
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Check queue
redis-cli lpush analytics_events '{ "event": "Hello, Black Creek Farm!" }'
```

## Common Issues

**Port 8080 in use?** Add to `application.yml`:
```yaml
server:
  port: 8081
```