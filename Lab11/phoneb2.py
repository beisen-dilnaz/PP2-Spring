import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="phonebook_db",
    user="phonebook_user",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Searching pattern
def search():
    pattern = input("Search (name or phone): ")
    cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s OR phone ILIKE %s", (f"%{pattern}%", f"%{pattern}%"))
    for row in cur.fetchall():
        print(row)

# Insert or update user
def insert_or_update():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("SELECT * FROM phonebook WHERE username = %s", (name,))
    if cur.fetchone():
        cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (phone, name))
    else:
        cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("Saved.")

# Insert many users
def insert_many():
    n = int(input("How many users: "))
    for _ in range(n):
        name = input("Name: ")
        phone = input("Phone: ")
        if phone.isdigit() and 10 <= len(phone) <= 15:
            insert_or_update()
        else:
            print(f"Invalid phone for {name}: {phone}")

# Paginated query
def paginate():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))
    cur.execute("SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
    for row in cur.fetchall():
        print(row)

# Delete user
def delete():
    key = input("Delete by name or phone: ")
    cur.execute("DELETE FROM phonebook WHERE username = %s OR phone = %s", (key, key))
    conn.commit()
    print("Deleted.")

# Menu
while True:
    print("\n1. Search\n2. Insert/Update\n3. Insert Many\n4. Paginate\n5. Delete\n6. Exit")
    c = input("Choice: ")
    if c == '1': search()
    elif c == '2': insert_or_update()
    elif c == '3': insert_many()
    elif c == '4': paginate()
    elif c == '5': delete()
    elif c == '6': break

cur.close()
conn.close()
