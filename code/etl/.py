import pandas as pd
import mysql.connector
import re

def etl_pipeline(data_path):
    try:
        df = pd.read_csv(data_path, encoding='unicode_escape')

        # 1. Cleaning InvoiceNo and StockCode (Handling mixed types)
        def extract_numeric(value):
            if isinstance(value, (int, float)):
                return str(int(value))
            elif isinstance(value, str):
                match = re.search(r'\d+', value)
                if match:
                    return match.group(0)
                else:
                    return None
            else:
                return None

        df['InvoiceNo'] = df['InvoiceNo'].apply(extract_numeric)
        df['StockCode'] = df['StockCode'].apply(extract_numeric)

        df.dropna(subset=['InvoiceNo', 'StockCode'], inplace=True)

        df['InvoiceNo'] = df['InvoiceNo'].astype(str)
        df['StockCode'] = df['StockCode'].astype(str)

        # 2. Other Cleaning and Data Type Conversion
        df.dropna(subset=['CustomerID'], inplace=True)
        df.drop_duplicates(inplace=True, subset=['InvoiceNo', 'StockCode', 'InvoiceDate'])

        df['CustomerID'] = df['CustomerID'].astype(int)
        df['Quantity'] = df['Quantity'].astype(int)
        df['Country'] = df['Country'].astype(str)
        df['UnitPrice'] = df['UnitPrice'].astype(float)
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], dayfirst=True)
        df['InvoiceDate'] = df['InvoiceDate'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # 3. Transformation
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

        return df

    except FileNotFoundError:
        print(f"Error: File not found at {data_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# 1. Process Data (Pandas)
data_file = "Online Retail 1.csv"  # Replace with your CSV file path
cleaned_df = etl_pipeline(data_file)

if cleaned_df is not None:
    print("Cleaned and transformed data:")
    print(f"Number of rows after cleaning: {len(cleaned_df)}")

    # 2. MySQL Connection and Database Setup
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",  # Or your MySQL server's IP
            user="root",
            password="Vikky@3043"  # Your MySQL password
        )
        mycursor = mydb.cursor()

        # Create database if it doesn't exist (or use an existing one)
        mycursor.execute("CREATE DATABASE IF NOT EXISTS vighneshgannedi")
        mycursor.execute("USE vighneshgannedi")

        # Create transactions table if it doesn't exist
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                InvoiceNo VARCHAR(255),
                StockCode VARCHAR(255),
                Description TEXT,
                Quantity INT,
                Country VARCHAR(255),
                UnitPrice DECIMAL(10, 2),
                CustomerID INT,
                InvoiceDate DATETIME,
                TotalPrice DECIMAL(10, 2),
                Cancelled BOOLEAN,
                PRIMARY KEY (InvoiceNo, StockCode, InvoiceDate)
            )
        """)
        mydb.commit()

    except mysql.connector.Error as err:
        print(f"MySQL Error (Database/Table): {err}")
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
        exit()

    # 3. Load Data to MySQL
    try:
        columns = ", ".join(cleaned_df.columns)
        placeholders = ", ".join(["%s"] * len(cleaned_df.columns))
        sql = f"INSERT INTO transactions ({columns}) VALUES ({placeholders})"
        mycursor.executemany(sql, cleaned_df.values.tolist())  # Use executemany

        mydb.commit()
        print("Data loaded successfully to MySQL.")

    except mysql.connector.Error as err:
        print(f"MySQL Error (Data Load): {err}")
        mydb.rollback()
    except Exception as e:
        print(f"An error occurred: {e}")
        mydb.rollback()
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

else:
    print("ETL pipeline failed.")
