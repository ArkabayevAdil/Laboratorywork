import psycopg2
import csv

# 🔌 Подключение к базе данных
conn = psycopg2.connect(
    database="mydb",
    user="postgres",
    password="20062008",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# 🧱 Создание таблицы, если она не существует
cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        phone VARCHAR(20) NOT NULL
    );
""")
conn.commit()

# 📥 Загрузка контактов из CSV-файла
def insert_from_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # пропустить заголовок
            for row in reader:
                cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
        conn.commit()
        print("📥 Данные из CSV успешно добавлены.")
    except Exception as e:
        print("❌ Ошибка при чтении CSV:", e)

# ✍️ Ручной ввод контакта
def insert_from_input():
    name = input("Введите имя контакта: ")
    phone = input("Введите номер телефона: ")
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("✅ Контакт успешно добавлен.")

# ♻️ Обновление существующего контакта
def update_contact():
    contact_id = input("Введите ID контакта, который хотите обновить: ")
    new_name = input("Новое имя: ")
    new_phone = input("Новый номер телефона: ")
    cur.execute("UPDATE phonebook SET name = %s, phone = %s WHERE id = %s", (new_name, new_phone, contact_id))
    conn.commit()
    print("♻️ Контакт успешно обновлён.")

# 🔍 Поиск по имени или номеру
def query_with_filter():
    keyword = input("Введите имя или номер для поиска: ")
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s OR phone ILIKE %s", (f'%{keyword}%', f'%{keyword}%'))
    rows = cur.fetchall()
    if not rows:
        print("🔍 Ничего не найдено.")
    else:
        for row in rows:
            print(row)

# ❌ Удаление контакта
def delete_contact():
    contact_id = input("Введите ID контакта для удаления: ")
    cur.execute("DELETE FROM phonebook WHERE id = %s", (contact_id,))
    conn.commit()
    print("❌ Контакт успешно удалён.")

# 📤 Экспорт контактов в CSV-файл
def export_to_csv(file_path="insert.csv"):
    cur.execute("SELECT name, phone FROM phonebook")
    rows = cur.fetchall()

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'phone'])  # заголовок
        writer.writerows(rows)

    print(f"📄 Контакты экспортированы в файл: {file_path}")

# 📋 Главное меню
def menu():
    while True:
        print("\n📱 МЕНЮ ТЕЛЕФОННОЙ КНИГИ:")
        print("1 - Загрузить данные из CSV")
        print("2 - Добавить контакт вручную")
        print("3 - Обновить контакт")
        print("4 - Поиск контакта")
        print("5 - Удалить контакт")
        print("6 - Выйти из программы")
        print("7 - Экспортировать контакты в файл insert.csv")

        choice = input("Выберите действие (1–7): ")

        if choice == '1':
            path = input("Введите путь к CSV-файлу (например: insert.csv): ")
            insert_from_csv(path)
        elif choice == '2':
            insert_from_input()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_with_filter()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("👋 Выход из программы...")
            break
        elif choice == '7':
            export_to_csv()
        else:
            print("❗ Неверный выбор. Попробуйте снова.")

# ▶️ Запуск программы
if __name__ == "__main__":
    menu()
    cur.close()
    conn.close()
