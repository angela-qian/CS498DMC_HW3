import time
import requests

for endpoint in ["insert-fast", "insert-safe"]:
    total = 0

    for i in range(500):
        data = {
            "VIN (1-10)": f"TEST_{endpoint}_{i}",  # use unique identifier
            "Make": "TESLA",
            "Model": "TEST",
            "City": "TEST",
            "Model Year": 2026
        }

        start = time.perf_counter()
        requests.post(f"http://localhost:8000/{endpoint}", json=data)
        total += time.perf_counter() - start

    print(endpoint, "average latency:", total / 500 * 1000, "ms")
