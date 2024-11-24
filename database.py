import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Definir caminho do banco
DB_PATH = '/app/data/cards.db'
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Classe de usuário para Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password_hash, is_admin):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        
        if not user:
            return None
        return User(user[0], user[1], user[2], user[3])

# Inicialização do banco de dados
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Tabela de usuários
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL
        )
    ''')
    
    # Tabela de cards
    c.execute('''
        CREATE TABLE IF NOT EXISTS cards
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         category TEXT NOT NULL,
         description TEXT NOT NULL,
         image_url TEXT NOT NULL,
         link TEXT NOT NULL,
         created_at DATETIME NOT NULL,
         position INTEGER)
    ''')
    
    # Criar usuário admin padrão se não existir
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not c.fetchone():
        create_user('admin', 'admin123', is_admin=True)
    
    conn.commit()
    conn.close()
    print(f"Banco de dados inicializado em: {DB_PATH}")

# Funções relacionadas a usuários
def create_user(username, password, is_admin=False):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    hashed_password = generate_password_hash(password)
    try:
        c.execute('''
            INSERT INTO users (username, password, is_admin, created_at)
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_password, is_admin, datetime.now()))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

# Funções relacionadas a cards
def get_cards():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM cards ORDER BY created_at ASC')
    cards = c.fetchall()
    conn.close()
    return cards

def get_card_by_id(card_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
    card = c.fetchone()
    conn.close()
    return card

def get_categories():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT DISTINCT category FROM cards ORDER BY category')
    categories = [row[0] for row in c.fetchall()]
    conn.close()
    return categories

def add_card(title, category, description, image_url, link):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM cards')
    position = c.fetchone()[0] + 1
    
    c.execute('''
        INSERT INTO cards (title, category, description, image_url, link, created_at, position)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, category, description, image_url, link, datetime.now(), position))
    conn.commit()
    conn.close()

def update_card(card_id, title, category, description, image_url, link):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE cards 
        SET title = ?, category = ?, description = ?, image_url = ?, link = ?
        WHERE id = ?
    ''', (title, category, description, image_url, link, card_id))
    conn.commit()
    conn.close()

def delete_card(card_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM cards WHERE id = ?', (card_id,))
    conn.commit()
    conn.close()

def generate_cards_html(card_ids=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if card_ids:
        placeholders = ','.join('?' * len(card_ids))
        c.execute(f'SELECT * FROM cards WHERE id IN ({placeholders}) ORDER BY created_at ASC', card_ids)
    else:
        c.execute('SELECT * FROM cards ORDER BY created_at ASC')
    
    cards = c.fetchall()
    conn.close()

    html = ""
    for i, card in enumerate(cards, 1):
        html += f'''
<!-- Card {i} -->
<a href="{card[5]}" class="card-item">
    <div class="img-container">
        <img src="{card[4]}" alt="{card[1]}">
    </div>
    <span class="designer">{card[2]}</span>
    <h3>{card[1]}</h3>
    <p>{card[3]}</p>
    <div class="arrow">
        <i class="fas fa-arrow-right card-icon"></i>
    </div>
</a>
'''
    return html