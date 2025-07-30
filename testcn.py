import psycopg2
from psycopg2 import OperationalError

DATABASE_URL = "postgresql://postgres:Ntruobgdoi91%40%21@db.dikrxyeyoarybnxrlflm.supabase.co:5432/postgres?sslmode=require"

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Kết nối thành công!")
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("PostgreSQL version:", version)
    cur.close()
    conn.close()
except OperationalError as e:
    print("Lỗi kết nối:", e)
