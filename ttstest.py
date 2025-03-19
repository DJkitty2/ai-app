import psutil

# Get total physical memory in bytes
total_memory_bytes = psutil.virtual_memory().total

# Convert to gigabytes
total_memory_gb = total_memory_bytes / (1024 ** 3)
model = "gemma3:1b"

if total_memory_gb < 10:
    print("under 10")
    print("keeping gemma3:1b")
else:
    print("over 10")
    model = "gemma3:12b"
    print("using gemma3:12b")
