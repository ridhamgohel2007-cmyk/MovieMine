"""
MovieMine MySQL Migration & Setup Utility
Run this script to initialize or migrate the database to a live MySQL instance.

Usage:
  python backend/database/mysql_setup.py
"""

import os
import sys
from pathlib import Path
import pymysql

backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from config import Config
from database.seed import seed_database

def setup_mysql():
    print("=" * 65)
    print(">> MovieMine: MySQL Database Setup & Initialization")
    print("=" * 65)

    host = Config.MYSQL_HOST
    port = int(Config.MYSQL_PORT)
    user = Config.MYSQL_USER
    password = Config.MYSQL_PASSWORD
    db_name = Config.MYSQL_DB

    print(f"Connecting to MySQL server at {host}:{port} with user '{user}'...")

    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset="utf8mb4"
        )
        with conn.cursor() as cursor:
            print(f"Creating database '{db_name}' if not exists...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.execute(f"USE {db_name};")
            print(f"Database '{db_name}' is ready.")

        conn.commit()
        conn.close()

        # Update environment to use MySQL
        os.environ["DATABASE_URL"] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
        os.environ["FORCE_SQLITE"] = "false"

        print("Executing schema and seeding data into MySQL...")
        seed_database(force_refresh=False)
        print("[SUCCESS] MySQL setup and data seeding completed successfully!")

    except pymysql.err.OperationalError as e:
        print(f"[ERROR] Could not connect to MySQL server: {e}")
        print("Tip: Ensure MySQL / XAMPP / WampServer is running on port 3306.")
    except Exception as e:
        print(f"[ERROR] MySQL setup failed: {e}")

if __name__ == "__main__":
    setup_mysql()
