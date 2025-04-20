import psycopg2
import csv
from tabulate import tabulate

conn = psycopg2.connect(
    host="localhost",
    dbname="LAB11",
    user="postgres",
    password="20062008",
    port=5432
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebookss (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        surname VARCHAR(50) NOT NULL,
        phone VARCHAR(20) UNIQUE NOT NULL
    );
""")
conn.commit()

def insert_user():
    name = input("Enter first name: ").strip()
    surname = input("Enter surname: ").strip()
    phone = input("Enter phone number: ").strip()

    if not name or not surname or not phone:
        print("❌ Name, surname, and phone are required.")
        return

    cur.execute("""
        INSERT INTO phonebookss (name, surname, phone)
        VALUES (%s, %s, %s)
        ON CONFLICT (phone)
        DO UPDATE SET name = EXCLUDED.name, surname = EXCLUDED.surname;
    """, (name, surname, phone))
    conn.commit()
    print("✅ User saved or updated.")


def find_users():
    pattern = input("Search pattern (name, surname or phone): ").strip()
    cur.execute("""
        SELECT * FROM phonebookss
        WHERE name ILIKE %s OR surname ILIKE %s OR phone ILIKE %s
    """, (f"%{pattern}%", f"%{pattern}%", f"%{pattern}%"))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="grid"))

def delete_user():
    target = input("Enter name, surname or phone to delete: ").strip()
    cur.execute("""
        DELETE FROM phonebookss
        WHERE name = %s OR surname = %s OR phone = %s
    """, (target, target, target))
    conn.commit()
    print("🗑️ Deleted (if existed).")

def show_all():
    cur.execute("SELECT * FROM phonebookss")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="grid"))

def insert_many_users():
    names = input("Enter first names (comma-separated): ").split(",")
    surnames = input("Enter surnames (comma-separated): ").split(",")
    phones = input("Enter phones (comma-separated): ").split(",")

    if len(names) != len(surnames) or len(names) != len(phones):
        print("❌ All lists must have the same length!")
        return

    for name, surname, phone in zip(names, surnames, phones):
        name = name.strip()
        surname = surname.strip()
        phone = phone.strip()

        if phone.isdigit() and len(phone) == 11 and phone.startswith("87"):
            cur.execute("""
                INSERT INTO phonebookss (name, surname, phone)
                VALUES (%s, %s, %s)
                ON CONFLICT (phone)
                DO UPDATE SET name = EXCLUDED.name, surname = EXCLUDED.surname;
            """, (name, surname, phone))
        else:
            print(f"❌ Invalid phone: {phone}")
    conn.commit()
    print("✅ All valid users inserted or updated.")

def paginate_users():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))
    cur.execute("SELECT * FROM phonebookss ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="grid"))

while True:
    print("""
    Menu:
    1. Insert user
    2. Find users
    3. Delete user
    4. Show all
    5. Insert many users
    6. Paginate users
    7. Exit
    """)
    choice = input(">>> ").strip()
    if choice == "1":
        insert_user()
    elif choice == "2":
        find_users()
    elif choice == "3":
        delete_user()
    elif choice == "4":
        show_all()
    elif choice == "5":
        insert_many_users()
    elif choice == "6":
        paginate_users()
    elif choice == "7":
        break

cur.close()
conn.close()