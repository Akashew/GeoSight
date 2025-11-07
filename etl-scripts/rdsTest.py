import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing RDS connection...")
print(f"Host: {os.getenv('DB_HOST')}")
print(f"Database: {os.getenv('DB_NAME')}")

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )
    
    print("✅ Connected successfully!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM earthquakes;")
    count = cursor.fetchone()[0]
    print(f"Current earthquakes in database: {count}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")