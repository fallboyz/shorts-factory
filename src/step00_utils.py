import os
import logging

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
