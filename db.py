import os
import sys
from sqlalchemy import create_engine

# Lấy DATABASE_URL từ biến môi trường
DATABASE_URL = os.environ.get("DATABASE_URL")

# ✅ In ra rõ ràng URL đang dùng
print("📌 DATABASE_URL từ môi trường:", repr(DATABASE_URL), file=sys.stderr)

# ✅ Kiểm tra nếu bị sai
if not DATABASE_URL:
    raise ValueError("❌ Không tìm thấy DATABASE_URL!")

if "port" in DATABASE_URL.lower():
    raise ValueError("🚫 DATABASE_URL hiện tại chứa chữ 'port'. Hãy sửa lại giá trị trong Render Environment!")

# Nếu dùng format cũ
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

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
