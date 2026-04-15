import sqlite3

DB_FILE = "edge_platform.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create Users table (for RBAC testing)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    
    # Create Videos table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        uploader_role TEXT NOT NULL,
        summary TEXT,
        extracted_tools TEXT,
        extracted_parts TEXT,
        filepath TEXT NOT NULL
    )
    ''')
    
    # Insert default mock users
    try:
        cursor.execute("INSERT INTO users (username, role) VALUES ('technician_01', 'TECHNICIAN')")
        cursor.execute("INSERT INTO users (username, role) VALUES ('expert_joe', 'EXPERT')")
    except sqlite3.IntegrityError:
        pass # Users already exist
        
    conn.commit()
    conn.close()
    print("SQLite Database initialized successfully.")

if __name__ == "__main__":
    init_db()
