from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

load_dotenv(PROJECT_ROOT / ".env")


def get_setting(name):
    value = os.getenv(name)

    if value:
        return value

    try:
        import streamlit as st
        return st.secrets.get(name)
    except Exception:
        return None


DB_HOST = get_setting("DB_HOST")
DB_PORT = get_setting("DB_PORT")
DB_USER = get_setting("DB_USER")
DB_PASSWORD = get_setting("DB_PASSWORD")
DB_NAME = get_setting("DB_NAME")