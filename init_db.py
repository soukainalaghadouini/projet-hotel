import sqlite3

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

# Créer les tables
cursor.executescript("""
DROP TABLE IF EXISTS Chambre;
DROP TABLE IF EXISTS TypeChambre;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Hotel;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Concerner;

CREATE TABLE Hotel (
    idHotel INTEGER PRIMARY KEY,
    nomHotel TEXT,
    ville TEXT
);

CREATE TABLE Client (
    idClient INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom_complet TEXT,
    Email TEXT
);

CREATE TABLE TypeChambre (
    idType INTEGER PRIMARY KEY,
    designation TEXT,
    prix REAL
);

CREATE TABLE Chambre (
    idChambre INTEGER PRIMARY KEY,
    idHotel INTEGER,
    idType INTEGER,
    FOREIGN KEY(idHotel) REFERENCES Hotel(idHotel),
    FOREIGN KEY(idType) REFERENCES TypeChambre(idType)
);

CREATE TABLE Reservation (
    Id_Reservation INTEGER PRIMARY KEY AUTOINCREMENT,
    idClient INTEGER,
    Date_arrivee TEXT,
    Date_depart TEXT,
    FOREIGN KEY(idClient) REFERENCES Client(idClient)
);

CREATE TABLE Concerner (
    Id_Reservation INTEGER,
    Id_Chambre INTEGER,
    FOREIGN KEY(Id_Reservation) REFERENCES Reservation(Id_Reservation),
    FOREIGN KEY(Id_Chambre) REFERENCES Chambre(idChambre)
);
""")

# Insertion de données exemple
cursor.execute("INSERT INTO Hotel VALUES (1, 'Hotel Riviera', 'Nice')")
cursor.execute("INSERT INTO Hotel VALUES (2, 'Hotel Montagne', 'Chamonix')")

cursor.execute("INSERT INTO TypeChambre VALUES (10, 'Simple', 100.00)")
cursor.execute("INSERT INTO TypeChambre VALUES (20, 'Double', 150.00)")

cursor.execute("INSERT INTO Chambre VALUES (1000, 1, 10)")
cursor.execute("INSERT INTO Chambre VALUES (1001, 2, 20)")

conn.commit()
conn.close()
