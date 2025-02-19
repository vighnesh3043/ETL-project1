Assume data is already loaded

##Connect to the database 
USE vighnesh;  
##Replace 'vighnesh' with your database name


##Indexes (add if they don't exist, modify if needed)
CREATE INDEX idx_customer_id ON transactions (CustomerID);
CREATE INDEX idx_invoice_date ON transactions (InvoiceDate);
CREATE INDEX idx_stock_code ON transactions (StockCode);
CREATE INDEX idx_country ON transactions (Country);



##Customer Summary Table
CREATE TABLE IF NOT EXISTS customer_summary (
    CustomerID INT PRIMARY KEY,
    FirstPurchaseDate DATETIME,
    LastPurchaseDate DATETIME,
    TotalPurchases INT,
    TotalAmountSpent DECIMAL(15, 2),
    AverageOrderValue DECIMAL(10, 2)
);

##Indexes for customer_summary
CREATE INDEX idx_last_purchase ON customer_summary (LastPurchaseDate);


##Product Summary Table
CREATE TABLE IF NOT EXISTS product_summary (
    StockCode VARCHAR(255) PRIMARY KEY,
    TotalUnitsSold INT,
    TotalRevenue DECIMAL(15, 2),
    AveragePrice DECIMAL(10, 2)
);

##Indexes for product_summary
-- (StockCode is already the primary key)


###Analytics Views

##Customer Purchase History View
CREATE OR REPLACE VIEW customer_purchase_history AS
SELECT
    ct.CustomerID,
    ct.InvoiceNo,
    ct.StockCode,
    ct.Description,
    ct.Quantity,
    ct.UnitPrice,
    ct.InvoiceDate,
    ct.TotalPrice
FROM
    transactions ct  -- Use your existing table name
ORDER BY
    ct.CustomerID, ct.InvoiceDate;

##Product Sales Overview View
CREATE OR REPLACE VIEW product_sales_overview AS
SELECT
    ct.StockCode,
    ct.Description,
    SUM(ct.Quantity) AS TotalUnitsSold,
    SUM(ct.TotalPrice) AS TotalRevenue,
    AVG(ct.UnitPrice) AS AveragePrice
FROM
    transactions ct  -- Use your existing table name
GROUP BY
    ct.StockCode, ct.Description;

-- c. Basic Customer Segments View (by purchase frequency)
CREATE OR REPLACE VIEW customer_segments AS
WITH CustomerPurchaseCounts AS (
    SELECT
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS PurchaseFrequency
    FROM
        transactions  -- Use your existing table name
    GROUP BY
        CustomerID
)
SELECT
    cpc.CustomerID,
    cpc.PurchaseFrequency,
    CASE
        WHEN cpc.PurchaseFrequency > 10 THEN 'Frequent Buyer'
        WHEN cpc.PurchaseFrequency > 3 THEN 'Regular Buyer'
        ELSE 'Occasional Buyer'
    END AS CustomerSegment
FROM
    CustomerPurchaseCounts cpc;



##Run these after creating the tables and views

##Customer Summary Table 
INSERT INTO customer_summary (CustomerID, FirstPurchaseDate, LastPurchaseDate, TotalPurchases, TotalAmountSpent, AverageOrderValue)
SELECT
    CustomerID,
    MIN(InvoiceDate),
    MAX(InvoiceDate),
    COUNT(DISTINCT InvoiceNo),
    SUM(TotalPrice),
    AVG(TotalPrice)
FROM
    transactions  
GROUP BY
    CustomerID;


##Product Summary Table 
INSERT INTO product_summary (StockCode, TotalUnitsSold, TotalRevenue, AveragePrice)
SELECT
    StockCode,
    SUM(Quantity),
    SUM(TotalPrice),
    AVG(UnitPrice)
FROM
    transactions 
GROUP BY
    StockCode;
