import os
from sqlalchemy import create_engine
import sys

# ⚠️ Lấy DATABASE_URL từ biến môi trường
DATABASE_URL = os.environ.get("DATABASE_URL")
print("📌 DEBUG DATABASE_URL:", repr(DATABASE_URL), file=sys.stderr)

# ✅ Bắt lỗi nếu vẫn chứa chữ "port"
if DATABASE_URL is None:
    raise ValueError("❌ DATABASE_URL không tồn tại!")
if "port" in DATABASE_URL.lower():
    raise ValueError("🚫 DATABASE_URL chứa từ 'port' thay vì số! Hãy kiểm tra lại trong Render.")

# ✅ Fix URL nếu dùng sai format ban đầu (Heroku/Supabase)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

# ✅ Tạo engine
engine = create_engine(DATABASE_URL)

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
