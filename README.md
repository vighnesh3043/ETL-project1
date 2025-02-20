# **ETL Pipeline and FastAPI API**

## **Overview**
This project implements an **ETL (Extract, Transform, Load) pipeline** using **Python, Pandas, and MySQL** to process retail transaction data. Additionally, a **FastAPI** application provides an API to retrieve customer summaries and product sales insights.

## **Features**
- **ETL Pipeline**: Cleans and loads data from CSV into MySQL.
- **MySQL Database**: Stores structured transaction data.
- **FastAPI Application**: Provides RESTful APIs for querying data.

## **Setup Instructions**
### **1. Prerequisites**
Ensure the following are installed:
- Python **3.12.3**
- MySQL Server
- MySQL Workbench
- Required Python dependencies
- Make sure the dataset is in CSV format for better results

### **2. Install Dependencies**
Run the following command to install required packages:
```sh
pip install pandas mysql-connector-python fastapi uvicorn
```

### **3. MySQL Setup**
#### **a. Install MySQL Server**
Download and install MySQL from [MySQL Official Site](https://dev.mysql.com/downloads/).

#### **b. Create Database and Tables**
Create a database using MySQL Workbench or the command line:
```sql
CREATE DATABASE yourdatabase;
USE yourdatabase;
```
**Note:** The ETL script will automatically create the required database and tables.

### **4. Running the FastAPI Application**
Start the FastAPI app:
```sh
uvicorn main:app --reload
```
**Note:** Ensure the ETL script and FastAPI app run in the same environment.

### **5. Access the API**
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### **6. Database Configuration**
Modify the credentials in your script as needed:
```python
DB_HOST = "e.g:123.0.0.1"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "your_database_name"
```

## **API Endpoints**
### **1. Get Customer Summary**
- **Endpoint:** `GET /customer_summary`
- **Query Parameter:** `customer_id` (optional, int)
- **Example Request:**
  ```sh
  GET http://127.0.0.1:8000/customer_summary?customer_id=12345
  ```
- **Response Example:**
  ```json
  [
    {
      "CustomerID": 12345,
      "TotalSpent": 500.75,
      "TotalOrders": 15,
      "LastPurchaseDate": "2025-01-15 14:30:00"
    }
  ]
  ```

### **2. Get Product Sales Overview**
- **Endpoint:** `GET /product_sales`
- **Query Parameter:** `product_code` (optional, string)
- **Example Request:**
  ```sh
  GET http://127.0.0.1:8000/product_sales?product_code=85123A
  ```
- **Response Example:**
  ```json
  [
    {
      "StockCode": "85123",
      "TotalSold": 150,
      "TotalRevenue": 1200.50,
      "LastSaleDate": "2025-02-18 10:00:00"
    }
  ]
  ```

## **Sample Queries**
### **1. Retrieve All Customers Summary**
```sh
GET http://127.0.0.1:8000/customer_summary
```

### **2. Retrieve Data for a Specific Customer**
```sh
GET http://127.0.0.1:8000/customer_summary?customer_id=12345
```

### **3. Retrieve All Product Sales Data**
```sh
GET http://127.0.0.1:8000/product_sales
```

### **4. Retrieve Sales Data for a Specific Product**
```sh
GET http://127.0.0.1:8000/product_sales?product_code=85123
```

## **Conclusion**
This project provides an efficient ETL pipeline and a RESTful API for analyzing customer and product sales data. 🚀
