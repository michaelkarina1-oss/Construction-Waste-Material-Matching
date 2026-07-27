# -*- coding: utf-8 -*-
"""
SiteSync Setup & Seed Script
Automates database creation, schema setup, and mock data injection for SiteSync.
"""
import os
import time
import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Database Connection Settings (Fallback to defaults if env vars not set)
DB_SERVER = os.getenv("DB_SERVER", "localhost,1433")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "YourStrongPassword123!")
DB_NAME = os.getenv("DB_NAME", "SiteSyncDB")
DB_DRIVER = os.getenv("DB_DRIVER", "{ODBC Driver 18 for SQL Server}")

DB_CONN_STRING_MASTER = (
    f"DRIVER={DB_DRIVER};"
    f"SERVER={DB_SERVER};"
    f"DATABASE=master;"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    f"TrustServerCertificate=yes;"
    f"Connection Timeout=15;"
)

def run_mega_setup():
    print("🚀 Starting SiteSync Setup & Seeding process...")
    print(f"🔌 Connecting to SQL Server at: {DB_SERVER}...")

    try:
        # Step 1: Database Recreation (Drop if exists & Create fresh)
        with pyodbc.connect(DB_CONN_STRING_MASTER, autocommit=True) as conn:
            cursor = conn.cursor()

            print(f"🧹 Resetting database [{DB_NAME}] if it exists...")
            cursor.execute(f"""
                IF EXISTS (SELECT * FROM sys.databases WHERE name = N'{DB_NAME}')
                BEGIN
                    ALTER DATABASE [{DB_NAME}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
                    DROP DATABASE [{DB_NAME}];
                END
            """)

            print(f"🛠️  Creating fresh database: [{DB_NAME}]...")
            cursor.execute(f"CREATE DATABASE [{DB_NAME}];")
            print("✅ Database created successfully!")

        time.sleep(2)

        # Step 2: Connect to the newly created database
        conn_string_new_db = DB_CONN_STRING_MASTER.replace("DATABASE=master;", f"DATABASE={DB_NAME};")

        with pyodbc.connect(conn_string_new_db, autocommit=True) as conn:
            cursor = conn.cursor()

            print("\n🏗️  Step 3: Creating primary requests table (t_ConstructionPool)...")
            cursor.execute("""
                CREATE TABLE dbo.t_ConstructionPool (
                    [Id] INT IDENTITY(1,1) PRIMARY KEY,
                    [CompanyName] NVARCHAR(100) NOT NULL,
                    [ContractorName] NVARCHAR(100) NOT NULL,
                    [SiteName] NVARCHAR(100) NOT NULL,
                    [Phone] VARCHAR(20) NOT NULL,
                    [ActionType] VARCHAR(20) NOT NULL,
                    [MaterialType] NVARCHAR(50) NOT NULL,
                    [Quantity] INT NOT NULL,
                    [Status] NVARCHAR(20) DEFAULT N'פעיל',
                    [CreatedAt] DATETIME DEFAULT GETDATE()
                );
            """)

            print("📜 Step 4: Creating match history table (t_MatchHistory)...")
            cursor.execute("""
                CREATE TABLE dbo.t_MatchHistory (
                    [MatchId] INT IDENTITY(1,1) PRIMARY KEY,
                    [GiverId] INT NOT NULL,
                    [ReceiverId] INT NOT NULL,
                    [MaterialType] NVARCHAR(50) NOT NULL,
                    [QuantityMatched] INT NOT NULL,
                    [MatchDate] DATETIME DEFAULT GETDATE(),
                    FOREIGN KEY ([GiverId]) REFERENCES dbo.t_ConstructionPool([Id]),
                    FOREIGN KEY ([ReceiverId]) REFERENCES dbo.t_ConstructionPool([Id])
                );
            """)
            print("✅ Database schema initialized!")

            # Step 3: Inject Mock Data (Seed)
            print("\n💉 Step 5: Injecting initial demo data...")

            poc_data = [
                {"CompanyName": "דניה סיבוס בע\"מ", "ContractorName": "אילן מזרחי", "SiteName": "פרויקט מגדלי הים, חיפה", "Phone": "052-4445566", "ActionType": "DISPOSAL", "MaterialType": "בטון גרוס / מצע", "Quantity": 45},
                {"CompanyName": "אשטרום קבלנות", "ContractorName": "יוסי כהן", "SiteName": "שכונת הרקפות, כרמיאל", "Phone": "054-1112233", "ActionType": "DISPOSAL", "MaterialType": "אדמה גסה", "Quantity": 80},
                {"CompanyName": "אלקטרה בנייה", "ContractorName": "רפי אהרוני", "SiteName": "מתחם ההייטק, תל אביב", "Phone": "050-9998877", "ActionType": "DISPOSAL", "MaterialType": "פסולת בניין נקייה", "Quantity": 30},
                {"CompanyName": "קבוצת תדהר", "ContractorName": "עופר לוי", "SiteName": "קניון המחר, נהריה", "Phone": "053-7776655", "ActionType": "DISPOSAL", "MaterialType": "חול נקי", "Quantity": 15},
                {"CompanyName": "שפיר הנדסה", "ContractorName": "מיכאל גבאי", "SiteName": "סלילת כביש עוקף, קריות", "Phone": "052-8889900", "ActionType": "COLLECTION", "MaterialType": "בטון גרוס / מצע", "Quantity": 50},
                {"CompanyName": "סולל בונה", "ContractorName": "אביב אוחנה", "SiteName": "עבודות פיתוח תשתית, עכו", "Phone": "054-5556677", "ActionType": "COLLECTION", "MaterialType": "אדמה גסה", "Quantity": 120},
                {"CompanyName": "א.מ.צ. שיווק תשתיות", "ContractorName": "גדי ישראלי", "SiteName": "מילוי פארק תעשייה, קורן", "Phone": "050-2223344", "ActionType": "COLLECTION", "MaterialType": "פסולת בניין נקייה", "Quantity": 25},
                {"CompanyName": "בנייני העיר הלבנה", "ContractorName": "ניר חסון", "SiteName": "יציקות יסודות, קרית אתא", "Phone": "055-6661122", "ActionType": "COLLECTION", "MaterialType": "חול נקי", "Quantity": 40}
            ]

            sql_insert = """
                INSERT INTO t_ConstructionPool (CompanyName, ContractorName, SiteName, Phone, ActionType, MaterialType, Quantity, Status)
                VALUES (?, ?, ?, ?, ?, ?, ?, N'פעיל')
            """

            for item in poc_data:
                cursor.execute(
                    sql_insert,
                    item["CompanyName"], item["ContractorName"], item["SiteName"],
                    item["Phone"], item["ActionType"], item["MaterialType"], item["Quantity"]
                )

            print(f"📊 Successfully inserted {len(poc_data)} initial mock records!")
            print("\n🎯 Setup completed successfully! System ready for demo.")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")

if __name__ == "__main__":
    run_mega_setup()