import psycopg2

# 1 Функция, создающая структуру БД (таблицы).
def create_db(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(40) NOT NULL,
                surname VARCHAR(40) NOT NULL,
                email VARCHAR(40) NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_book(
                phone_id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES client(client_id),
                phone CHAR(12)
            );
        """)
        conn.commit()
    except psycopg2.Error as e:

        pass

# 2 Функция, позволяющая добавить нового клиента.
def add_client(conn, name, surname, email, phones=None):
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO client(name, surname, email) values (%s, %s, %s) RETURNING client_id;
        """, (name, surname, email))
        client_id = cur.fetchone()[0]
        if phones:
            for phone in phones:
                cur.execute("""
                    INSERT INTO phone_book(client_id, phone) VALUES(%s, %s);
                """, (client_id, phone))
        conn.commit()
    except psycopg2.Error as e:

        pass

# 3 Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, client_id, phone):
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO phone_book(client_id, phone) VALUES(%s, %s);
        """, (client_id, phone))
        conn.commit()
    except psycopg2.Error as e:

        pass

# 4 Функция, позволяющая изменить данные о клиенте.
def change_client(conn, client_id, name=None, surname=None, email=None, phones=None):
    try:
        cur = conn.cursor()
        if name:
            cur.execute("""
                UPDATE client SET name = %s WHERE client_id = %s;
            """, (name, client_id))
        if surname:
            cur.execute("""
                UPDATE client SET surname = %s WHERE client_id = %s;
            """, (surname, client_id))
        if email:
            cur.execute("""
                UPDATE client SET email = %s WHERE client_id = %s;
            """, (email, client_id))
        if phones:
            for phone_id, phone_number in phones.items():
                cur.execute("""
                    UPDATE phone_book SET phone = %s WHERE phone_id = %s;
                """, (phone_number, phone_id))
        conn.commit()
    except psycopg2.Error as e:

        pass

# 5 Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(conn, client_id, phone):
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM phone_book WHERE client_id = %s AND phone = %s;
        """, (client_id, phone))
        conn.commit()
    except psycopg2.Error as e:

        pass

# 6 Функция, позволяющая удалить существующего клиента.
def delete_client(conn, client_id):
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM phone_book WHERE client_id = %s;
            DELETE FROM client WHERE client_id = %s;
        """, (client_id, client_id))
        conn.commit()
    except psycopg2.Error as e:

        pass

# 7 Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(conn, **kwargs):
    cur = conn.cursor()
    conditions = []
    values = []
    for key, value in kwargs.items():
        conditions.append(f"{key} = %s")
        values.append(value)
    query = "SELECT * FROM client WHERE " + " AND ".join(conditions)
    cur.execute(query, values)
    rows = cur.fetchall()
    return rows




with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    create_db(conn)
    add_client(conn, 'name', 'surname', 'email', phones=None)
    add_phone(conn, 1, '89999999999')
    change_client(conn, 1, name=None, surname=None, email=None, phones=None)
conn.close()

