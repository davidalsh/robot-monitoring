import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
REFRESH_FREQUENCY_HZ = int(os.environ.get("REFRESH_FREQUENCY_HZ", 10))
