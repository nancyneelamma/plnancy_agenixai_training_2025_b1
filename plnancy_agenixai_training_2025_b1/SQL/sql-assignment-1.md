##  SQL Database Design and Querying for a Library Management System

### Objective

To design, implement, and optimize a relational database for a library system using industry best practices. This assignment includes a pre-defined dataset for realistic testing and validation.

### Scenario

Design a Relational Data Model for a library system that manages books, authors, customers, and book transactions. The system must ensure data integrity, handle large datasets, and support complex queries.

---

### Tasks

**Task 1:** Design the Logical and Conceptual Data Model and ER Diagram.

**Task 2:** Create Pyshical data model on postgrsql database. Ensure proper use of: Primary and foreign keys. Constraints like NOT NULL, UNIQUE, and ON DELETE CASCADE.Make Sure to name database as: lms_db.

**Task3:** Generate synthetic data using Python and ingest it into postgrsql tables. this can be great exercise for python developers. For those who are new to python you can use chatgpt ask like: *create a python script to generate synthetic data insert commands for postgresql database for library management system data model which  that manages books, authors, customers, and book transactions* or customise it as per your data model design.

**Task4:** Write SQL queries to handle the following business insights and reporting requirements:

    1: Retrieve the top 5 most-issued books with their issue count.
    2: List books along with their authors that belong to the "Fantasy" genre, sorted by publication year in descending order.
    3: Identify the top 3 customers who have borrowed the most books.
    4: List all customers who have overdue books (assume overdue if ReturnDate is null and IssueDate is older than 30 days).
    5: Find authors who have written more than 3 books.
    6: Retrieve a list of authors who have books issued in the last 6 months.
    7. Calculate the total number of books currently issued and the percentage of books issued compared to the total available.
    8. Generate a monthly report of issued books for the past year, showing month, book count, and unique customer count.
    9: Add appropriate indexes to optimize queries.
    10:Analyze query execution plans for at least two queries using EXPLAIN and write your understanding from execution query plan in your words.
---
