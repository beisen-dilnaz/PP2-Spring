import psycopg2
import csv

# Connection with database
conn = psycopg2.connect(
    dbname="phonebook_db",
    user="phonebook_user",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Creating file
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()

# Inserting from csv file
def insert_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';') 
        next(reader)  
        for row in reader:
            full_name = row[0].strip() + " " + row[1].strip()
            phone = row[2].strip()
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (full_name, phone))
    conn.commit()
    print("s Data inserted from CSV.")

# Inserting from console
def insert_from_console():
    username = input("Enter full name: ")
    phone = input("Enter phone number: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    print(" Data inserted.")

# Updating user
def update_user():
    old_name = input("Enter current username: ")
    new_name = input("Enter new username (leave blank to skip): ")
    new_phone = input("Enter new phone (leave blank to skip): ")

    if new_name:
        cur.execute("UPDATE phonebook SET username = %s WHERE username = %s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (new_phone, new_name or old_name))
    conn.commit()
    print(" User updated.")

# Query phonebook
def query_data():
    keyword = input("Search by name or phone: ")
    cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s OR phone ILIKE %s", (f'%{keyword}%', f'%{keyword}%'))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Deleting user
def delete_user():
    key = input("Delete by name or phone: ")
    cur.execute("DELETE FROM phonebook WHERE username = %s OR phone = %s", (key, key))
    conn.commit()
    print(" User(s) deleted.")

# Menu
def menu():
    create_table()
    while True:
        print("\n📞 PHONEBOOK MENU")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update user")
        print("4. Query phonebook")
        print("5. Delete user")
        print("6. Exit")

        choice = input("Choose option: ")
        if choice == '1':
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_user()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_user()
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

    cur.close()
    conn.close()

# Starting the program
if __name__ == "__main__":
    menu()