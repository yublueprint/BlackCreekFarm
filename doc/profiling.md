# ⚙️ Django Profiling Guide

Performance profiling tools for Django: **Silk Profiler** for request/query analysis and **Memory Profiler** for memory usage tracking.

---

## 🧩 Silk Profiler

**Track HTTP requests, database queries, and execution times**

### Setup

1. **Enable in `settings.py`:**
   ```python
   ENABLE_SILK = True  # Set to False after testing
   ```

2. **Access dashboard:**  
   [http://127.0.0.1:8000/silk/](http://127.0.0.1:8000/silk/)

3. **Disable after profiling:**
   ```python
   ENABLE_SILK = False
   ```

---

## 🧠 Memory Profiler

**Measure function-level memory consumption**

### Usage

Add `@profile` decorator to target functions:

```python
from memory_profiler import profile

@profile
def retrieve_recent_activity():
    data = []
    for i in range(10000):
        data.append(i * 2)
    return data
```

### Run with profiling:
```bash
python -m memory_profiler manage.py runserver
```

### Understanding Results

| Column | Description |
|--------|-------------|
| **Mem usage** | Total process memory at that line |
| **Increment** | Memory change from previous line |
| **Occurrences** | Execution count for that line |

---

## ⚠️ Post-Profiling Cleanup

**Always disable profiling in production:**

- ✅ Remove `@profile` decorators
- ✅ Set `ENABLE_SILK = False`
- ✅ Stop memory profiler execution

> 💡 **Tip:** Leaving profiling enabled causes significant performance overhead.