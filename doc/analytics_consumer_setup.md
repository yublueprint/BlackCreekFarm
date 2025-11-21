# Analytics Consumer - Complete Setup Guide

Step-by-step guide for installing all required software and running the **analytics-consumer** service locally.

---

## Overview

- **Service**: `analytics-consumer`
- **Java Version**: 21 (LTS)
- **IDE**: IntelliJ IDEA
- **Infrastructure**: Redis (Docker)
- **Architecture**: Scheduled consumer polling Redis queue for analytics events

---

## Table of Contents

1. [Install Java 21](#step-1-install-java-21)
2. [Install IntelliJ IDEA](#step-2-install-intellij-idea)
3. [Install Docker Desktop](#step-3-install-docker-desktop)
4. [Open Project in IntelliJ](#step-4-open-project-in-intellij)
5. [Configure Java SDK in IntelliJ](#step-5-configure-java-sdk-in-intellij)
6. [Configure Project Settings](#step-6-configure-project-settings)
7. [Setup Redis](#step-7-setup-redis)
8. [Run the Application](#step-8-run-the-application)
9. [Test the Consumer](#step-9-test-the-consumer)
10. [Troubleshooting](#troubleshooting)

---

## STEP 1: Install Java 21

### Download Java 21

1. Visit [Adoptium.net](https://adoptium.net/temurin/releases/)
2. Select the following options:
   - **Operating System**: Your OS (Windows/macOS/Linux)
   - **Architecture**: x64
   - **Package Type**: JDK
   - **Version**: 21 (LTS)

3. Click **Download** button

### Install Java 21

**Windows:**
1. Run the downloaded `.msi` installer
2. Click **Next** through the installation wizard
3. Important: Check ✅ **Set JAVA_HOME variable**
4. Check ✅ **Add to PATH**
5. Click **Install**
6. Wait for installation to complete
7. Click **Finish**

**macOS:**
1. Open the downloaded `.pkg` file
2. Click **Continue** through the installation
3. Click **Install**
4. Enter your password when prompted
5. Click **Close** when finished

### Verify Java Installation

Open a **new** terminal/command prompt (important: close any old ones):

```bash
java -version
```

**Expected output:**
```
openjdk version "21.0.1" 2023-10-17 LTS
OpenJDK Runtime Environment Temurin-21.0.1+12 (build 21.0.1+12-LTS)
OpenJDK 64-Bit Server VM Temurin-21.0.1+12 (build 21.0.1+12-LTS, mixed mode, sharing)
```

If you see `java: command not found` or a different version, restart your computer and try again.

---

## STEP 2: Install IntelliJ IDEA

### Download IntelliJ IDEA

1. Visit [JetBrains IntelliJ IDEA Downloads](https://www.jetbrains.com/idea/download/)

2. Choose your edition:
   - **Community Edition** (Free) ← Recommended for this project

3. Click **Download** for your operating system

### Install IntelliJ IDEA

**Windows:**
1. Run the downloaded `.exe` installer
2. Click **Next**
3. Choose installation location (default is fine)
4. On the **Installation Options** screen, select:
   - ✅ **Create Desktop Shortcut**
   - ✅ **Update PATH variable** (add "bin" folder to PATH)
   - ✅ **Add "Open Folder as Project"** (adds context menu)
   - ✅ **`.java`** - Associate .java files with IntelliJ
5. Click **Next** → **Install**
6. Wait for installation (may take 2-3 minutes)
7. Check ✅ **Run IntelliJ IDEA**
8. Click **Finish**

**macOS:**
1. Open the downloaded `.dmg` file
2. Drag **IntelliJ IDEA** icon into the **Applications** folder
3. Open **Applications** folder
4. Double-click **IntelliJ IDEA**
5. If macOS shows a security warning:
   - Click **Cancel**
   - Go to **System Preferences → Security & Privacy**
   - Click **Open Anyway**
6. Click **Open** in the confirmation dialog

### First Launch Configuration

When you launch IntelliJ for the first time:

1. **Import Settings**: Select **Do not import settings** → Click **OK**

2. **Data Sharing**: Choose your preference (either option is fine)

3. **UI Theme**: 
   - Select **Light** or **Dark** (you can change this later)
   - Click **Next**

4. **Plugins**:
   - Leave defaults selected
   - Click **Next**

5. **Featured Plugins** screen:
   - Scroll down and find **Lombok**
   - Click **Install** next to Lombok
   - Wait for it to install
   - Click **Start using IntelliJ IDEA**

You should now see the IntelliJ IDEA welcome screen.

---

## STEP 3: Open Project in IntelliJ

### Locate Your Project

1. Open **IntelliJ IDEA**
2. On the welcome screen, click **Open**
3. Navigate to your project folder: `analytics-consumer/`
4. Click the **folder** (not any file inside it)
5. Click **OK**

IntelliJ will open the project and start indexing (you'll see a progress bar at the bottom).

### Wait for Indexing

**Important**: Let IntelliJ complete indexing before proceeding. You'll see messages like:
- "Indexing..."
- "Scanning files to index..."
- "Updating indices..."

This may take 1-3 minutes on first open. Wait until the progress bar disappears.

### Trust the Project

If prompted with "Trust and Open Project?":
1. Read the message
2. Click **Trust Project**

---

## STEP 4: Configure Java SDK in IntelliJ

This is the most critical step for ensuring the application runs correctly.

### Open Project Structure

1. Click **File** in the menu bar
2. Click **Project Structure...** (or press `Ctrl+Alt+Shift+S` on Windows/Linux, `Cmd+;` on macOS)

### Configure Project SDK

In the **Project Structure** dialog:

1. Click **Project** in the left sidebar

2. Look at **Project SDK** dropdown:

   **If Java 21 is listed:**
   - Select **21** from the dropdown
   - Skip to step 3

   **If Java 21 is NOT listed:**
   - Click the **Edit** dropdown → **Add SDK** → **Download JDK...**
   - In the popup:
     - **Version**: Select **21**
     - **Vendor**: Select **Eclipse Temurin (AdoptOpenJDK)**
     - **Location**: Leave default
   - Click **Download**
   - Wait for download to complete (1-2 minutes)
   - IntelliJ will automatically select the downloaded JDK

3. Set **Project language level**: Select **21 - Pattern matching for switch**

4. Verify settings look like this:
   ```
   Project SDK: 21 (java version "21.0.1")
   Project language level: 21 - Pattern matching for switch
   ```

5. Click **Apply** (bottom right)

### Configure Module SDK

Still in the **Project Structure** dialog:

1. Click **Modules** in the left sidebar
2. Click your module name (usually `analytics-consumer`)
3. Click the **Dependencies** tab
4. Look at **Module SDK**: Should show **<Project SDK> (java version "21.0.1")**
5. If it shows a different version, click the dropdown and select the Project SDK

6. Click **Apply** → **OK**

---

## STEP 5: Configure Project Settings

### Enable Annotation Processing (Required for Lombok)

1. Go to **File** → **Settings** (Windows/Linux) or **IntelliJ IDEA** → **Preferences** (macOS)
2. In the search box at the top, type: `annotation`
3. Click **Build, Execution, Deployment** → **Compiler** → **Annotation Processors**
4. Check ✅ **Enable annotation processing**
5. Verify these settings:
   - **Obtain processors from project classpath**: Selected
   - **Store generated sources relative to**: Module content root
6. Click **Apply**

### Reload Maven Dependencies

1. Look at the **right sidebar** of IntelliJ
2. Click the **Maven** tab (if not visible, go to **View** → **Tool Windows** → **Maven**)
3. In the Maven panel, click the **🔄 Reload All Maven Projects** icon (top left)
4. Wait for Maven to download dependencies (2-5 minutes on first time)

You'll see progress messages like:
```
Resolving dependencies...
Downloading: org.springframework.boot:spring-boot-starter:3.x.x
Downloaded: redis.clients:jedis:5.x.x
```

Wait until you see: **BUILD SUCCESS**

### Start Redis

Open the **Terminal** in IntelliJ (bottom panel) or use your system terminal:

```bash
# Start Redis using Docker Compose
docker-compose up -d
```

**Expected output:**
```
Creating network "analytics-consumer_default" with the default driver
Creating volume "analytics-consumer_redis-data" with default driver
Creating analytics-redis ... done
Creating redis-ui        ... done
```

### Verify Redis is Running

```bash
docker-compose ps
```

**Expected output:**
```
NAME              IMAGE                          STATUS
analytics-redis   redis:7-alpine                 Up (healthy)
redis-ui          redis-commander:latest         Up
```

### Test Redis Connection

```bash
docker exec -it analytics-redis redis-cli ping
```

**Expected output:**
```
PONG
```

If you see `PONG`, Redis is working correctly!

---

## STEP 6: Run the Application

### Locate the Main Class

1. In IntelliJ, navigate to: `src/main/java/`
2. Find the main application class (usually named `AnalyticsConsumerApplication.java`)
3. Open it

4. Verify it has these annotations:

```java
@EnableScheduling  // ← MUST have this for polling
@SpringBootApplication
public class AnalyticsConsumerApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(AnalyticsConsumerApplication.class, args);
    }
}
```

### Run the Application

**Method 1: Using IntelliJ Run Button (Recommended)**

1. In the `AnalyticsConsumerApplication.java` file, look for the **green ▶️ play button** next to:
   - The class name, OR
   - The `main` method

2. Click the **▶️ button**

3. Select **Run 'AnalyticsConsumerApplication'**

4. IntelliJ will compile and run the application

**Method 2: Using Maven**

In the IntelliJ Terminal:
```bash
./mvnw spring-boot:run
```

On Windows, use:
```bash
mvnw.cmd spring-boot:run
```

### Expected Console Output

When the application starts successfully, you should see:

```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v3.2.0)

2024-11-21 14:23:15.123  INFO 12345 --- [main] c.e.a.AnalyticsConsumerApplication       : Starting AnalyticsConsumerApplication
2024-11-21 14:23:16.456  INFO 12345 --- [main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port 8080
2024-11-21 14:23:17.789  INFO 12345 --- [main] c.e.a.AnalyticsConsumerApplication       : Started AnalyticsConsumerApplication in 2.5 seconds
2024-11-21 14:23:18.012  INFO 12345 --- [scheduling-1] c.e.a.consumer.RedisConsumer            : 📊 Polling Redis queue: analytics_events
2024-11-21 14:23:18.013  INFO 12345 --- [scheduling-1] c.e.a.consumer.RedisConsumer            : ⏳ Waiting for analytics events...
```

**Key indicators of success:**
- ✅ "Started AnalyticsConsumerApplication in X seconds"
- ✅ "Polling Redis queue: analytics_events"
- ✅ No error messages

### Stop the Application

To stop the running application:
- In IntelliJ: Click the **red ⏹️ stop button** in the Run panel
- Or press: `Ctrl+F2` (Windows/Linux) or `Cmd+F2` (macOS)

---

## STEP 9: Test the Consumer

Now let's verify the application is consuming events from Redis.

### Test 1: Send a Simple Event

Open a **new terminal** (not in IntelliJ) and run:

```bash
docker exec -it analytics-redis redis-cli LPUSH analytics_events "test-event-123"
```

**Expected IntelliJ console output:**
```
2024-11-21 14:25:30.456  INFO 12345 --- [scheduling-1] c.e.a.consumer.RedisConsumer : 📥 Received event from queue
2024-11-21 14:25:30.457  INFO 12345 --- [scheduling-1] c.e.a.consumer.RedisConsumer : Event data: test-event-123
2024-11-21 14:25:30.458  INFO 12345 --- [scheduling-1] c.e.a.processor.EventProcessor : ⚙️ Processing analytics event...
```

If you see these messages, **congratulations!** Your consumer is working!

### Test 2: Send a JSON Event

```bash
docker exec -it analytics-redis redis-cli LPUSH analytics_events '{"type":"page_view","userId":"user_123","page":"/dashboard","timestamp":"2024-11-21T14:30:00Z"}'
```

### Test 3: Send Multiple Events

```bash
docker exec -it analytics-redis redis-cli LPUSH analytics_events "event-1" "event-2" "event-3"
```

You should see three separate "Received event" messages in the console.

### Test 4: Monitor Queue Using Redis Commander

1. Open your browser
2. Go to: [http://localhost:8081](http://localhost:8081)
3. You should see the Redis Commander interface
4. Click on the database (usually **db0**)
5. Look for the **analytics_events** key
6. You can add events here by clicking **Add Key**

### Verify Queue is Empty

After the consumer processes all events:

```bash
docker exec -it analytics-redis redis-cli LLEN analytics_events
```

**Expected output:**
```
(integer) 0
```

This means the queue is empty and all events have been processed!

---

## Troubleshooting

### Problem: Java version error when running

**Error message:**
```
Error: LinkageError occurred while loading main class
```

**Solution:**
1. Go to **File** → **Project Structure** → **Project**
2. Verify **Project SDK** is set to **Java 21**
3. Click **Modules** → **Dependencies**
4. Verify **Module SDK** is set to **Project SDK**
5. Click **OK**
6. Go to **File** → **Invalidate Caches** → **Invalidate and Restart**

### Problem: Cannot resolve Lombok annotations

**Error message:**
```
Cannot resolve symbol 'log'
Cannot find getter methods
```

**Solution:**
1. Install Lombok plugin:
   - **File** → **Settings** → **Plugins**
   - Search for "Lombok"
   - Click **Install**
   - Click **OK**
   - Restart IntelliJ

2. Enable annotation processing:
   - **File** → **Settings** → **Build, Execution, Deployment** → **Compiler** → **Annotation Processors**
   - Check ✅ **Enable annotation processing**
   - Click **Apply** → **OK**

3. Reload Maven:
   - **Maven** panel (right sidebar) → Click **🔄 Reload All Maven Projects**

4. Rebuild project:
   - **Build** → **Rebuild Project**

### Problem: Cannot connect to Redis

**Error message:**
```
Unable to connect to Redis: Connection refused
```

**Solution:**
1. Check Docker is running:
   ```bash
   docker ps
   ```
   
2. If no containers are listed, start Redis:
   ```bash
   docker compose up -d
   ```

3. Verify Redis is healthy:
   ```bash
   docker compose ps
   ```
   Status should show "Up (healthy)"

4. Test Redis connection:
   ```bash
   docker exec -it analytics-redis redis-cli ping
   ```
   Should return: `PONG`

5. If still not working, restart Redis:
   ```bash
   docker compose restart redis
   ```

### Problem: Port 8080 already in use

**Error message:**
```
Web server failed to start. Port 8080 was already in use.
```

**Solution Option 1: Change the port**
1. Open `src/main/resources/application.yml`
2. Add or modify:
   ```yaml
   server:
     port: 8081
   ```
3. Save and restart the application

**Solution Option 2: Kill the process using port 8080**

Windows:
```bash
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

macOS:
```bash
lsof -ti:8080 | xargs kill -9
```

### Problem: Maven dependencies not downloading

**Error message:**
```
Cannot resolve symbol 'SpringApplication'
Package org.springframework.boot does not exist
```

**Solution:**
1. Check internet connection
2. In IntelliJ Maven panel: Click **🔄 Reload All Maven Projects**
3. If still failing, clean and reimport:
   ```bash
   ./mvnw clean install
   ```
4. If still failing, delete Maven cache:
   - Close IntelliJ
   - Delete folder: `~/.m2/repository/`
   - Reopen IntelliJ
   - Reload Maven projects

### Problem: Application starts but doesn't poll Redis

**Symptoms:**
- Application starts successfully
- No "Polling Redis queue" messages appear
- Events in Redis are not consumed

**Solution:**
1. Verify `@EnableScheduling` annotation exists:
   - Open `AnalyticsConsumerApplication.java`
   - Ensure `@EnableScheduling` is present above the class

2. Check scheduler configuration:
   - Open your consumer class (e.g., `RedisConsumer.java`)
   - Verify the method has `@Scheduled` annotation:
     ```java
     @Scheduled(fixedRate = 5000)
     public void pollRedis() { ... }
     ```

3. Check application logs for scheduler errors

4. Verify Redis configuration in `application.yml` has correct values

---

## Quick Reference

### Daily Workflow

1. **Start Docker Desktop** (if not already running)

2. **Start Redis**:
   ```bash
   docker-compose up -d
   ```

3. **Open IntelliJ** and open the project

4. **Run the application**: Click ▶️ next to `AnalyticsConsumerApplication`

5. **Test with events**:
   ```bash
   docker exec -it analytics-redis redis-cli LPUSH analytics_events "test"
   ```

6. **Stop application**: Click ⏹️ in IntelliJ

7. **Stop Redis** (when done for the day):
   ```bash
   docker-compose down
   ```

### Useful Commands

```bash
# Check Redis queue length
docker exec -it analytics-redis redis-cli LLEN analytics_events

# View all events in queue
docker exec -it analytics-redis redis-cli LRANGE analytics_events 0 -1

# Clear entire queue
docker exec -it analytics-redis redis-cli DEL analytics_events

# Monitor Redis in real-time
docker exec -it analytics-redis redis-cli MONITOR

# View Docker logs
docker-compose logs -f redis

# Restart Redis
docker-compose restart redis

# Stop everything
docker-compose down
```

---