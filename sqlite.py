import sqlite3

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Client (
    Id_Client INTEGER PRIMARY KEY,
    Nom_complet TEXT,
    Adresse TEXT,
    Ville TEXT,
    Code_postal INTEGER,
    Email TEXT,
    Num_telephone TEXT
);
""")
conn.commit()
conn.close()
