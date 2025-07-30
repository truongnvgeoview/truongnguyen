import psycopg2
import pandas as pd
from datetime import datetime

# Thông tin kết nối Supabase
DB_CONFIG = {
    "host": "db.dikrxyeyoarybnxrlflm.supabase.co",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "Ntruobgdoi91@!",
    "sslmode": "require"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# ===== INVENTORY =====

def fetch_inventory():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM inventory ORDER BY model", conn)
    conn.close()
    return df

def add_inventory(model, imei, gia_nhap, tinh_trang):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO inventory (model, imei, gia_nhap, tinh_trang)
        VALUES (%s, %s, %s, %s)
    """, (model, imei, gia_nhap, tinh_trang))
    conn.commit()
    cur.close()
    conn.close()

def delete_inventory(imei):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM inventory WHERE imei = %s", (imei,))
    conn.commit()
    cur.close()
    conn.close()

# ===== BANHANG =====

def fetch_sales():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM banhang ORDER BY ngay_ban DESC", conn)
    conn.close()
    return df

def sell_device(imei):
    conn = get_connection()
    cur = conn.cursor()

    # Lấy thông tin máy từ inventoryfrom sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Tạo engine
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
        # Lấy máy từ inventory
        result = conn.execute(text("SELECT * FROM inventory WHERE imei = :imei"), {"imei": imei}).fetchone()
        if result:
            conn.execute(text("""
                INSERT INTO banhang (model, imei, gia_nhap, tinh_trang, ngay_ban)
                VALUES (:model, :imei, :gia_nhap, :tinh_trang, CURRENT_DATE)
            """), dict(result))
            conn.execute(text("DELETE FROM inventory WHERE imei = :imei"), {"imei": imei})

    cur.execute("SELECT model, imei, gia_nhap, tinh_trang FROM inventory WHERE imei = %s", (imei,))
    device = cur.fetchone()

    if device:
        ngay_ban = datetime.now().strftime("%Y-%m-%d")
        # Chuyển sang bảng banhang
        cur.execute("""
            INSERT INTO banhang (model, imei, gia_nhap, tinh_trang, ngay_ban)
            VALUES (%s, %s, %s, %s, %s)
        """, (*device, ngay_ban))
        # Xoá khỏi kho
        cur.execute("DELETE FROM inventory WHERE imei = %s", (imei,))

    conn.commit()
    cur.close()
    conn.close()
