from dotenv import load_dotenv
import os

load_dotenv()

# ✅ In ra để kiểm tra chính xác
print("✅ DEBUG: DATABASE_URL =", os.getenv("DATABASE_URL"))

from sqlalchemy import create_engine, text
engine = create_engine(os.getenv("DATABASE_URL"))
