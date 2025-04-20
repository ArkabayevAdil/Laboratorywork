import psycopg2
import csv

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="LAB11",
    user="postgres",
    password="20062008",
    port=5432
)

conn.autocommit = True
cur = conn.cursor()

# --- Создание таблицы phonebook
cur.execute("""
CREATE TABLE IF NOT EXISTS phone (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL,
    user_phone VARCHAR(20) NOT NULL
);
""")

# --- Удаление предыдущих процедур и функций
cur.execute("DROP FUNCTION IF EXISTS search_pattern(TEXT);")
cur.execute("DROP PROCEDURE IF EXISTS insert_or_update_user(TEXT, TEXT);")
cur.execute("DROP PROCEDURE IF EXISTS insert_many_users(TEXT[][]);")
cur.execute("DROP FUNCTION IF EXISTS get_users(INT, INT);")
cur.execute("DROP PROCEDURE IF EXISTS delete_user_by_value(TEXT);")

# --- 1. Функция поиска по шаблону (username или phone)
cur.execute("""
CREATE OR REPLACE FUNCTION search_pattern(pattern TEXT)
RETURNS TABLE(id INT, username TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY 
    SELECT id, username, phone 
    FROM phone
    WHERE username ILIKE '%' || pattern || '%' 
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
""")

# --- 2. Процедура вставки одного пользователя (обновляет номер, если существует)
cur.execute("""
CREATE OR REPLACE PROCEDURE insert_or_update_user(username_param TEXT, phone_param TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phone WHERE user_name = username_param) THEN
        UPDATE phone SET user_phone = phone_param WHERE user_name = username_param;
    ELSE
        INSERT INTO phone(user_name, user_phone) VALUES(username_param, phone_param);
    END IF;
END;
$$;
""")

# --- 3. Процедура вставки списка пользователей, проверка номера
cur.execute("""
CREATE OR REPLACE PROCEDURE insert_many_users(users TEXT[][])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(users, 1) LOOP
        IF users[i][2] ~ '^\\d{11}$' THEN
            CALL insert_or_update_user(users[i][1], users[i][2]);
        ELSE
            RAISE NOTICE '❌ Invalid phone: %', users[i][2];
        END IF;
    END LOOP;
END;
$$;
""")

# --- 4. Функция постраничного вывода
cur.execute("""
CREATE OR REPLACE FUNCTION get_users(limit_num INT, offset_num INT)
RETURNS TABLE(id INT, username TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY SELECT * FROM phone
    ORDER BY id
    LIMIT limit_num OFFSET offset_num;
END;
$$ LANGUAGE plpgsql;
""")

# --- 5. Процедура удаления по имени или номеру
cur.execute("""
CREATE OR REPLACE PROCEDURE delete_user_by_value(val TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phone WHERE username = val OR phone = val;
END;
$$;
""")

# --- Вызовы функций и процедур из Python ---

def call_search():
    val = input("Введите часть имени или номера: ")
    cur.execute("SELECT * FROM search_pattern(%s)", (val,))
    for row in cur.fetchall():
        print(row)

def call_insert():
    name = input("Имя: ")
    phone = input("Номер: ")
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))

def call_many():
    n = int(input("Сколько пользователей добавить: "))
    users = []
    for _ in range(n):
        name = input("Имя: ")
        phone = input("Номер: ")
        users.append(["", name, phone])
    cur.execute("CALL insert_many_users(%s)", (users,))

def call_delete():
    val = input("Введите имя или номер для удаления: ")
    cur.execute("CALL delete_user_by_value(%s)", (val,))
    print("🗑️ Удалено, если существовало.")

def call_paginate():
    lim = int(input("Лимит: "))
    off = int(input("Смещение (offset): "))
    cur.execute("SELECT * FROM get_users(%s, %s)", (lim, off))
    for row in cur.fetchall():
        print(row)

# --- Главное меню ---
while True:
    print("\nМеню:")
    print("1 - Добавить/обновить пользователя")
    print("2 - Добавить список пользователей")
    print("3 - Поиск по шаблону")
    print("4 - Удаление по имени или номеру")
    print("5 - Показать с лимитом и смещением")
    print("0 - Выход")

    choice = input("Выберите: ")
    if choice == "1":
        call_insert()
    elif choice == "2":
        call_many()
    elif choice == "3":
        call_search()
    elif choice == "4":
        call_delete()
    elif choice == "5":
        call_paginate()
    elif choice == "0":
        break
    else:
        print("Некорректный выбор.")

cur.close()
conn.close()