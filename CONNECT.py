import psycopg2

try:
    conn = psycopg2.connect(
        host="db.dikrxyeyoarybnxrlflm.supabase.co",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="Ntruobgdoi91@!",
        sslmode="require"
    )
    print("✅ Kết nối thành công đến PostgreSQL Supabase!")
    conn.close()

except Exception as e:
    print("❌ Lỗi khi kết nối:", e)
