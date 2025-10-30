# ⚙️ Django Profiling Usage Guide

This guide walks you through how to **verify**, **use**, and **analyze** profiling results
after successfully setting up **Django Silk** and **Memory Profiler** (we will use both of them)




--------------------------------------------------------------------------------------

### 🧩 Silk Profiler

1. **Enable profiling** in your `settings.py`:
   ENABLE_SILK = False
   **Set to True to enable profiling; switch back to False after testing**
2. http://127.0.0.1:8000/silk/ **Run your Django application and open the Silk dashboard**
3. After profiling is complete, disable it to avoid extra overhead:
   ENABLE_SILK = False

-------------------------------------------------------------------------------------

# 🧠 Django Memory Profiler Guide

This guide explains how to use the **Memory Profiler** in your Django project to measure
function-level memory usage and identify inefficiencies.


## ⚙️ Configuration Example

Add the `@profile` decorator to the function you want to analyze:

```python
from memory_profiler import profile

@profile
def retrieve_recent_activity():
    # Example code
    data = []
    for i in range(10000):
        data.append(i * 2)
    return data


## 📊 Interpreting Results

| Column | Meaning |
|---------|----------|
| **Mem usage** | The total memory used by the process at that line |
| **Increment** | The difference in memory from the previous line |
| **Occurrences** | Number of times that line of code was executed |

---

## ⚠️ Clean Up After Profiling

Once you finish profiling:

1. **Remove or comment out** all `@profile` decorators.  
2. **Stop running** with `memory_profiler` active.  
3. **Revert** any temporary debug or Silk changes.  

Leaving profiling enabled will increase runtime overhead and memory usage.
