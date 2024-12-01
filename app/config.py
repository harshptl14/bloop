import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database configuration
DB_PATH = os.path.join(BASE_DIR, "data", "workspace.db")

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) 