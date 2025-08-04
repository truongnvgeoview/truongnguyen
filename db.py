from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import text
import sys

# ✅ Bỏ biến môi trường đi, dùng URL hardcode để test chính xác lỗi
DATABASE_URL = "postgresql+psycopg2://postgres:Ntruobgdoi91%40%21@db.dikrxyeyoarybnxrlflm.supabase.co:5432/postgres?sslmode=require"
print("📌 DEBUG: USING HARDCODED DATABASE_URL", file=sys.stderr)

# ✅ Tạo engine
engine = create_engine(DATABASE_URL)

# ===== INVENTORY =====
def fetch_inventory():
    with engine.begin() as conn:
        return pd.read_sql("SELECT * FROM inventory ORDER BY model", conn)

def add_inventory(model, imei, gia_nhap, tinh_trang):
    with engine.begin() as conn:
        query = text("""
            INSERT INTO inventory (model, imei, gia_nhap, tinh_trang)
            VALUES (:model, :imei, :gia_nhap, :tinh_trang)
        """)
        conn.execute(query, {
            "model": model,
            "imei": imei,
            "gia_nhap": gia_nhap,
            "tinh_trang": tinh_trang
        })

def delete_inventory(imei):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM inventory WHERE imei = :imei"), {"imei": imei})

# ===== BÁN HÀNG =====
def fetch_sales():
    with engine.begin() as conn:
        return pd.read_sql("SELECT * FROM banhang ORDER BY ngay_ban DESC", conn)

def sell_device(imei):
    with engine.begin() as conn:
        result = conn.execute(text("SELECT * FROM inventory WHERE imei = :imei"), {"imei": imei}).fetchone()
        if result:
            conn.execute(text("""
                INSERT INTO banhang (model, imei, gia_nhap, tinh_trang, ngay_ban)
                VALUES (:model, :imei, :gia_nhap, :tinh_trang, CURRENT_DATE)
            """), dict(result))
            conn.execute(text("DELETE FROM inventory WHERE imei = :imei"), {"imei": imei})
