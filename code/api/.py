from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Optional
from contextlib import asynccontextmanager
import mysql.connector

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "Vikky@3043"
DB_NAME = "vighnesh"

mydb = None
mycursor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global mydb, mycursor
    try:
        print("Application started. Establishing database connection...")
        mydb = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        mycursor = mydb.cursor(dictionary=True)
        yield
    finally:
        print("Application shutting down. Closing database connection...")
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

app = FastAPI(lifespan=lifespan)

def fetch_data(query: str) -> List[Dict]:
    try:
        mycursor.execute(query)
        return mycursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Database query error: {err}")
        mydb.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

@app.get("/customer_summary")
async def get_customer_summary(customer_id: Optional[int] = Query(None, title="Customer ID", description="Enter a valid customer ID")):
    query = "SELECT * FROM customer_summary WHERE 1=1"
    if customer_id is not None:
        query += f" AND CustomerID = {customer_id}"
    customer_data = fetch_data(query)
    if not customer_data:
        raise HTTPException(status_code=404, detail="Customer summary not found")
    return customer_data

@app.get("/product_sales")
async def get_product_sales_overview(product_code: Optional[str] = Query(None, title="Product Code", description="Enter a valid product code")):
    query = "SELECT * FROM product_sales_overview WHERE 1=1"
    if product_code is not None:
        query += f" AND StockCode = '{product_code}'"
    product_data = fetch_data(query)
    if not product_data:
        raise HTTPException(status_code=404, detail="Product sales data not found")
    return product_data


