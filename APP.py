from sqlalchemy import create_engine, text
import pandas as pd

# Thay DATABASE_URL bằng chuỗi kết nối thực tế của bạn
DATABASE_URL = "postgresql://username:password@host:port/databasename"

# Tạo engine kết nối DB
engine = create_engine(DATABASE_URL)

def fetch_inventory():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM inventory"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

def add_inventory(model, imei, gia_nhap, tinh_trang):
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO inventory (model, imei, gia_nhap, tinh_trang) VALUES (:model, :imei, :gia_nhap, :tinh_trang)"
            ),
            {"model": model, "imei": imei, "gia_nhap": gia_nhap, "tinh_trang": tinh_trang},
        )
        conn.commit()

def delete_inventory(imei):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM inventory WHERE imei = :imei"), {"imei": imei})
        conn.commit()

def fetch_sales():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM sales"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

def sell_device(imei):
    with engine.connect() as conn:
        # Di chuyển dữ liệu thiết bị từ inventory sang sales (giả sử có trường phù hợp)
        conn.execute(text("""
            INSERT INTO sales (model, imei, gia_nhap, tinh_trang, sold_at)
            SELECT model, imei, gia_nhap, tinh_trang, NOW() FROM inventory WHERE imei = :imei
        """), {"imei": imei})

        conn.execute(text("DELETE FROM inventory WHERE imei = :imei"), {"imei": imei})

        conn.commit()
