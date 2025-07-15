import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "app.log")

logger = logging.getLogger("IslamicAdkApp")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# File handler
fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(ch)

# Print log file path
print(f"Logging to: {os.path.abspath(log_path)}")
