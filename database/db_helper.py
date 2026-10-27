import sqlite3

DB_NAME = "fastfood.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    conn.commit()
    conn.close()

def seed_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO categories (name) VALUES (?)", [
            ("🍔 Burgerlar",), ("🍟 Gazaklar",), ("🥤 Ichimliklar",)
        ])
        products = [
            (1, "Cheeseburger", 25000, "Mol go'shti, pishloq", "burger.jpg"),
            (1, "Double Burger", 35000, "Ikki hissa go'sht", "double.jpg"),
            (2, "Kartoshka Fri", 15000, "Ketchup bilan", "fries.jpg"),
            (3, "Coca-Cola 0.5L", 8000, "Muzdek", "cola.jpg")
        ]
        cursor.executemany("INSERT INTO products (category_id, name, price, description, image) VALUES (?, ?, ?, ?, ?)", products)
    conn.commit()
    conn.close()

def get_categories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    conn.close()
    return data

def get_products_by_category(category_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE category_id = ?", (category_id,))
    data = cursor.fetchall()
    conn.close()
    return data


def get_user_cart(user_id):
    """Foydalanuvchi savatidagi mahsulotlar va ularning umumiy ma'lumotlarini olish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.name, p.price, c.quantity 
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data


def add_to_cart(user_id, product_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()


    cursor.execute("SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    item = cursor.fetchone()

    if item:
        cart_id = item[0]  # Tupledagi 1-element: qator ID-si
        current_qty = item[1]  # Tupledagi 2-element: hozirgi soni
        new_quantity = current_qty + 1


        cursor.execute("UPDATE cart SET quantity = ? WHERE id = ?", (new_quantity, cart_id))
    else:
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)", (user_id, product_id))

    conn.commit()
    conn.close()


def clear_user_cart(user_id):
    """Foydalanuvchi savatini to'liq bo'shatish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()


    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()
