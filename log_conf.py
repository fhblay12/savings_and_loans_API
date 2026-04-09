import logging
import os

def init_logging():
    os.makedirs("logs", exist_ok=True)  # 👈 create folder if it doesn't exist
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s | %(asctime)s | %(name)-15s | %(funcName)s() | L%(lineno)-2d | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/app.log", mode='w')
        ]
    )