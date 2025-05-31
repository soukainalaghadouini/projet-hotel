-- Créer la base de données (si elle n'existe pas déjà)
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'HotelDB')
BEGIN
    CREATE DATABASE HotelDB;
END
GO

-- Utiliser la base de données
USE HotelDB;
GO

-- Supprimer les tables existantes dans le bon ordre (en respectant les dépendances)
IF OBJECT_ID('Concerner', 'U') IS NOT NULL DROP TABLE Concerner;
IF OBJECT_ID('Reservation', 'U') IS NOT NULL DROP TABLE Reservation;
IF OBJECT_ID('Chambre', 'U') IS NOT NULL DROP TABLE Chambre;
IF OBJECT_ID('Client', 'U') IS NOT NULL DROP TABLE Client;
IF OBJECT_ID('TypeChambre', 'U') IS NOT NULL DROP TABLE TypeChambre;
IF OBJECT_ID('Hotel', 'U') IS NOT NULL DROP TABLE Hotel;
GO

-- Créer la table Hotel
CREATE TABLE Hotel (
    idHotel INT PRIMARY KEY,
    nomHotel NVARCHAR(100),
    ville NVARCHAR(100)
);
GO

-- Créer la table Client
CREATE TABLE Client (
    idClient INT PRIMARY KEY,
    nomClient NVARCHAR(100),
    prenomClient NVARCHAR(100)
);
GO

-- Créer la table TypeChambre
CREATE TABLE TypeChambre (
    idType INT PRIMARY KEY,
    designation NVARCHAR(50),
    prix DECIMAL(10, 2)
);
GO

-- Créer la table Chambre
CREATE TABLE Chambre (
    idChambre INT PRIMARY KEY,
    idHotel INT FOREIGN KEY REFERENCES Hotel(idHotel),
    idType INT FOREIGN KEY REFERENCES TypeChambre(idType)
    -- Retiré idClient ici car une chambre n'a pas directement un client lié en permanence
);
GO

-- Créer la table Reservation
CREATE TABLE Reservation (
    Id_Reservation INT IDENTITY(1,1) PRIMARY KEY,
    idClient INT FOREIGN KEY REFERENCES Client(idClient),
    Date_arrivee DATE NOT NULL,
    Date_depart DATE NOT NULL
);
GO

-- Créer la table Concerner (relation entre Reservation et Chambre)
CREATE TABLE Concerner (
    Id_Reservation INT FOREIGN KEY REFERENCES Reservation(Id_Reservation),
    Id_Chambre INT FOREIGN KEY REFERENCES Chambre(idChambre),
    PRIMARY KEY (Id_Reservation, Id_Chambre)
);
GO

-- Insérer des données dans Hotel
INSERT INTO Hotel (idHotel, nomHotel, ville) VALUES
(1, 'Hotel Riviera', 'Nice'),
(2, 'Hotel Montagne', 'Chamonix');
GO

-- Insérer des données dans Client
INSERT INTO Client (idClient, nomClient, prenomClient) VALUES
(100, 'Dupont', 'Jean'),
(101, 'Martin', 'Claire');
GO

-- Insérer des données dans TypeChambre
INSERT INTO TypeChambre (idType, designation, prix) VALUES
(10, 'Simple', 100.00),
(20, 'Double', 150.00);
GO

-- Insérer des données dans Chambre
INSERT INTO Chambre (idChambre, idHotel, idType) VALUES
(1000, 1, 10),
(1001, 2, 20);
GO
