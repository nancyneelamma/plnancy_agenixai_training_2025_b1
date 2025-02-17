--Retrieve the top 5 most-issued books with their issue count.

SELECT bd.Book_Name,Count(btd.Purchase_ID) AS Issue_Count
FROM book_transaction_details btd 
JOIN book_details bd ON bd.Book_ID=btd.Book_ID 
WHERE btd.Status = 'Issued'
GROUP BY bd.Book_Name
ORDER BY Issue_Count DESC
LIMIT 5;

-- List books along with their authors that belong to the "Fantasy" genre, sorted by publication year in descending order.

SELECT Book_Name,Author_Name,Genre, 
EXTRACT(YEAR FROM Date_Published) AS Year_Published
FROM Book_Details 
WHERE Genre = 'Fantasy'
ORDER BY Year_Published DESC;

-- Identify the top 3 customers who have borrowed the most books.

SELECT CONCAT(cd.First_Name,' ',cd.Last_Name) AS Customer_Name,Count(btd.Purchase_ID) AS Borrowed
FROM book_transaction_details btd 
JOIN Customer_Details cd ON cd.Customer_ID=btd.Customer_ID 
WHERE btd.Status = 'Issued'
GROUP BY cd.Customer_ID
ORDER BY Borrowed DESC
LIMIT 3;

-- List all customers who have overdue books (assume overdue if ReturnDate is null and IssueDate is older than 30 days).

SELECT CONCAT(cd.First_Name,'',cd.Last_Name) AS Customer_Name,btd.Issued_Date,btd.Due_Date,btd.Status,bd.Book_Name
FROM book_transaction_details btd
JOIN Customer_Details cd ON cd.Customer_ID=btd.Customer_ID
JOIN book_details bd ON bd.Book_ID=btd.Book_ID 
WHERE btd.Return_Date IS NULL AND AGE(CURRENT_DATE,btd.Issued_Date) > INTERVAL '30 Days' 
ORDER BY Customer_Name;

-- Find authors who have written more than 3 books.

SELECT Count(DISTINCT bd.Book_ID) AS Book_Count, CONCAT(ad.First_Name,'',ad.Last_Name) AS Author_Name, STRING_AGG(bd.Book_Name, ',') AS Book_Names 
FROM Author_details ad
JOIN book_details bd ON ad.Book_ID = bd.Book_ID 
GROUP BY ad.First_Name,ad.Last_Name
HAVING Count(DISTINCT bd.Book_ID) > 3
ORDER BY Author_Name;

-- Retrieve a list of authors who have books issued in the last 6 months.

SELECT DISTINCT bd.Author_Name
FROM book_transaction_details btd
JOIN Book_Details bd ON btd.Book_ID=bd.Book_ID
WHERE btd.Issued_Date >= CURRENT_DATE - INTERVAL '6 months'
ORDER BY Author_Name;

-- Calculate the total number of books currently issued and the percentage of books issued compared to the total available.

SELECT Count(btd.Purchase_ID) AS Issued_Book,
(COUNT(btd.Book_ID) * 100.0 / SUM(bd.No_of_Copies)) AS Percentage
FROM book_transaction_details btd 
JOIN book_details bd ON bd.Book_ID=btd.Book_ID 
WHERE btd.Issued_Date IS NOT NULL;

-- Generate a monthly report of issued books for the past year,showing month, book count, and unique customer count.

SELECT STRING_AGG(bd.Book_Name, ',') AS Book_Names,
EXTRACT(MONTH FROM btd.Issued_Date) AS Month_Report,COUNT(btd.Book_ID) AS Book_Count,
COUNT(btd.Customer_ID) AS Unique_Customer_Count
FROM book_transaction_details btd 
Join Book_Details bd ON btd.Book_ID = bd.Book_ID
WHERE btd.Issued_Date >= CURRENT_DATE - INTERVAL '1 year' 
GROUP BY EXTRACT(MONTH FROM btd.Issued_Date)
ORDER BY Month_Report ASC;

-- Add appropriate indexes to optimize queries.

CREATE INDEX idx_Book_Details_Book_ID ON Book_Details(Book_ID);
CREATE INDEX idx_book_transaction_details_Status ON Book_Transaction_Details(Status);
CREATE INDEX idx_book_id_author_details ON Author_Details(Book_ID);
CREATE INDEX idx_customer_id_transaction_details ON Book_Transaction_Details(Customer_ID);
CREATE INDEX idx_employee_id_transaction_details ON Book_Transaction_Details(Employee_ID);
CREATE INDEX idx_issued_date ON Book_Transaction_Details(Issued_Date);
CREATE INDEX idx_return_date ON Book_Transaction_Details(Return_Date);

