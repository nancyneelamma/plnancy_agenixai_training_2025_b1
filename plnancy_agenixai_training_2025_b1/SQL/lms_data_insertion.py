import psycopg2
import random
import string
import datetime

def generate_random_string(length):
    """Generates a random string of specified length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_date(start_date, end_date):
    """Generates a random date within a given date range."""
    # Ensure that the start_date is earlier than end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date  # Swap if invalid range

    # Ensure there's a valid range between start and end dates
    if start_date == end_date:
        # Adjust the end date slightly to avoid having the same date
        end_date = end_date + datetime.timedelta(days=1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    if days_between_dates <= 0:  # In case the dates are still the same
        raise ValueError(f"Invalid date range: {start_date} to {end_date}")

    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

def generate_isbn():
    """Generates a valid ISBN-13 number."""
    isbn = "978-"
    for _ in range(9):
        isbn += str(random.randint(0, 9))
    isbn += "-"
    isbn += str(random.randint(0, 9))
    return isbn

def generate_unique_book_id(conn):
    """Generates a unique book ID using database query."""
    cursor = conn.cursor()
    is_unique = False
    while not is_unique:
        book_id = random.randint(10000, 30000)  # Increase the upper limit to avoid collisions more effectively
        cursor.execute("SELECT * FROM Book_Details WHERE Book_ID = %s", (book_id,))
        result = cursor.fetchone()
        if not result:
            is_unique = True
    return book_id

def generate_book_name():
    """Generates a more meaningful book name."""
    nouns = ["Dreams", "Shadows", "Whispers", "Soul", "Journey", "Fate", "Hope", "Time", "Silence", "Memory"]
    adjectives = ["Lost", "Hidden", "Broken", "Ancient", "Forgotten", "Silent", "Wandering", "Eternal", "Crimson", "Obsidian"]
    articles = ["The", "A"]

    article = random.choice(articles)
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)

    return f"{article} {adjective} {noun}"

def generate_author_details(existing_author_ids):
    """Generates random author ID, first and last names, ensuring uniqueness."""
    first_names = ["John", "Jane", "David", "Sarah", "Michael", "Emily", "Daniel", "James", "Robert", "Mary"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

    # Ensure that the Author_ID is unique
    author_id = random.randint(40000, 90000)  # Generate random Author_ID
    while author_id in existing_author_ids:
        author_id = random.randint(30000, 50000)  # Regenerate if the Author_ID already exists
    existing_author_ids.add(author_id)

    first_name = random.choice(first_names)
    last_name = random.choice(last_names).replace("'", "''")  # Escape single quotes in last names
    return author_id, first_name, last_name

def generate_customer_details(existing_customer_ids, existing_emails):
    """Generates random customer ID, first and last names, email, phone number, and address."""
    # Ensure the generated customer ID is unique
    customer_id = random.randint(100000, 200000)
    while customer_id in existing_customer_ids:
        customer_id = random.randint(100000, 200000)  # Regenerate if the Customer_ID already exists
    existing_customer_ids.add(customer_id)

    first_names = ["Alex", "Emma", "Lucas", "Olivia", "Ethan", "Sophia", "Mason", "Isabella", "Noah", "Ava"]
    last_names = ["Taylor", "Brown", "Harris", "King", "Clark", "Lewis", "Walker", "Scott", "Hall", "Allen"]
    phone_numbers = [f"{random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"]  # Format phone numbers

    # Ensure the generated email is unique
    while True:
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(['gmail', 'hotmail', 'yahoo'])}.com"
        if email not in existing_emails:
            existing_emails.add(email)
            break

    phone_number = random.choice(phone_numbers)

    # Generating random address details
    street_names = ["Oak St", "Maple Ave", "Pine Rd", "Elm St", "Birch Ln", "Cedar Blvd", "Willow Way", "Ash Dr", "Cherry Ct", "Redwood Blvd"]
    cities = ["Springfield", "Riverton", "Lincoln", "Madison", "Greenfield", "Brighton", "Fairview", "Oakwood", "Highland Park", "Summitville"]
    countries = ["USA", "Canada", "UK", "Australia", "India", "Germany", "France", "Japan", "Italy", "Brazil"]

    street = random.choice(street_names)
    city = random.choice(cities)
    country = random.choice(countries)
    address = f"{random.randint(100, 999)} {street}, {city}, {country}"

    return customer_id, first_name, last_name, email, phone_number, address

def generate_librarian_details(existing_employee_ids):
    """Generates random librarian ID, first and last names, and phone number."""
    # Ensure the employee ID is unique
    employee_id = random.randint(300000, 400000)
    while employee_id in existing_employee_ids:
        employee_id = random.randint(300000, 400000)  # Regenerate if the Employee_ID already exists
    existing_employee_ids.add(employee_id)
    
    first_names = ["Ethan", "Olivia", "Noah", "Ava", "Liam", "Emma", "Mason", "Isabella", "Lucas", "Sophia"]
    last_names = ["Clark", "Harris", "Taylor", "Martinez", "Garcia", "Robinson", "Lee", "Young", "Hall", "Wilson"]
    phone_numbers = [f"{random.randint(100, 999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"]  # Librarian phone numbers
    phone_number = random.choice(phone_numbers)
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    return employee_id, first_name, last_name, phone_number

def generate_book_transaction_details(book_id, customer_id, employee_id):
    """Generates SQL INSERT statement for Book_Transaction_Details."""
    # Generate the issued_date first
    issued_date = generate_random_date(datetime.date(2021, 1, 1), datetime.date(2024, 12, 31)) if random.choice([True, False]) else None

    # Initialize return_date and due_date as None
    return_date = None
    due_date = None
    
    if issued_date:
        # Ensure that the due_date is always after the issued_date
        due_date = generate_random_date(issued_date, datetime.date(2024, 12, 31)) if random.choice([True, False]) else generate_random_date(issued_date, issued_date + datetime.timedelta(days=30))  # Set a default due date (30 days after issue)
        
    # Ensure the return_date is after the issued_date and before or equal to the due_date
    if due_date:
        return_date = generate_random_date(issued_date, due_date) if random.choice([True, False]) else None

    # Set the status and ensure the logic for the conditions
    today = datetime.date.today()
    if issued_date is None:  # If no issue date, return_date and due_date are NULL
        return_date_str = "NULL"
        due_date_str = "NULL"
        status = "Not Issued"
    else:
        if return_date is None:  # Book is not returned yet
            if due_date and today == due_date:
                status = "Overdue"
            else:
                status = "Issued"
            return_date_str = "NULL"
            due_date_str = f"'{due_date.strftime('%Y-%m-%d')}'" if due_date else "NULL"
        else:  # Book is returned
            if return_date <= due_date:
                status = "Returned"
                return_date_str = f"'{return_date.strftime('%Y-%m-%d')}'"
            else:
                status = "Overdue"
                return_date_str = f"'{return_date.strftime('%Y-%m-%d')}'"
            due_date_str = f"'{due_date.strftime('%Y-%m-%d')}'" if due_date else "NULL"
    
    issued_date_str = f"'{issued_date.strftime('%Y-%m-%d')}'" if issued_date else "NULL"

    transaction_details_insert = f"""
    INSERT INTO Book_Transaction_Details (Book_ID, Customer_ID, Employee_ID, Issued_Date, Return_Date, Due_Date, Status) 
    VALUES ({book_id}, {customer_id}, {employee_id}, {issued_date_str}, {return_date_str}, {due_date_str}, '{status}');
    """
    return transaction_details_insert


def generate_book_details(conn, existing_emails, existing_author_ids, existing_employee_ids, existing_customer_ids):
    """Generates SQL INSERT statements for Book_Details, Author_Details, Customer_Details, Librarian_Details, and Book_Transaction_Details."""
    book_id = generate_unique_book_id(conn)
    book_name = generate_book_name()
    author_id, author_first_name, author_last_name = generate_author_details(existing_author_ids)
    customer_id, customer_first_name, customer_last_name, customer_email, customer_phone, customer_address = generate_customer_details(existing_customer_ids, existing_emails)
    genre = random.choice(["Fiction", "Non-Fiction", "Mystery", "Romance", "Fantasy", "Science Fiction", "Biography", "History", "Horror", "Self-Help"])
    date_published = generate_random_date(datetime.date(1900, 1, 1), datetime.date(2023, 12, 31))
    no_of_copies = random.randint(1, 10)
    isbn = generate_isbn()
    cost = round(random.uniform(100.00, 3000.00), 2)

    employee_id, librarian_first_name, librarian_last_name, librarian_phone = generate_librarian_details(existing_employee_ids)

    # Insert statements for all four tables
    book_details_insert = f"INSERT INTO Book_Details (Book_ID, Book_Name, Author_Name, Genre, Date_Published, No_of_Copies, ISBN, Cost) VALUES ({book_id}, '{book_name}', '{author_first_name} {author_last_name}', '{genre}', '{date_published}', {no_of_copies}, '{isbn}', {cost});\n"
    author_details_insert = f"INSERT INTO Author_Details (Author_ID, Book_ID, First_Name, Last_Name) VALUES ({author_id}, {book_id}, '{author_first_name}', '{author_last_name}');\n"
    customer_details_insert = f"INSERT INTO Customer_Details (Customer_ID, First_Name, Last_Name, Email, Phone_No, Address) VALUES ({customer_id}, '{customer_first_name}', '{customer_last_name}', '{customer_email}', '{customer_phone}', '{customer_address}');\n"
    librarian_details_insert = f"INSERT INTO Librarian_Details (Employee_ID, First_Name, Last_Name, Phone_No) VALUES ({employee_id}, '{librarian_first_name}', '{librarian_last_name}', '{librarian_phone}');\n"

    # Generate Book_Transaction_Details for the book
    transaction_details_insert = generate_book_transaction_details(book_id, customer_id, employee_id)

    # Combine all SQL insert statements
    return book_details_insert + author_details_insert + customer_details_insert + librarian_details_insert + transaction_details_insert


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",  # Replace with your actual host
    database="lms_db",   # Replace with your actual database name
    user="postgres",   # Replace with your actual username
    password="newpassword"  # Replace with your actual password
)
cursor = conn.cursor()

# Track emails to ensure uniqueness
existing_emails = set()
# Track author IDs to ensure uniqueness
existing_author_ids = set()
# Track employee IDs to ensure uniqueness
existing_employee_ids = set()
# Track customer IDs to ensure uniqueness
existing_customer_ids = set()

# Generate and execute insert statements
for i in range(300):  # Generate 300 book records
    insert_statements = generate_book_details(conn, existing_emails, existing_author_ids, existing_employee_ids, existing_customer_ids)
    if insert_statements.strip():  # Only execute if the query isn't empty
        print(f"Inserting record {i+1}")
        cursor.execute(insert_statements)

conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully!")