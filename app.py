import streamlit as st
import sqlite3
from datetime import date

# Connexion à la base de données
conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

st.title("🏨 Système de Réservation d’Hôtel")

menu = st.sidebar.radio("Menu", [
    "Voir les Clients",
    "Ajouter Client",
    "Voir Réservations",
    "Chambres Disponibles"
])

# Voir les clients
if menu == "Voir les Clients":
    st.subheader("👤 Liste des Clients")
    cursor.execute("SELECT * FROM Client")
    rows = cursor.fetchall()
    st.table(rows)

# Ajouter un client
elif menu == "Ajouter Client":
    st.subheader("➕ Ajouter un Client")
    with st.form("form_client"):
        nom = st.text_input("Nom complet")
        email = st.text_input("Email")
        if st.form_submit_button("Ajouter"):
            if nom.strip() == "" or email.strip() == "":
                st.error("Veuillez remplir tous les champs.")
            else:
                cursor.execute("INSERT INTO Client (Nom_complet, Email) VALUES (?, ?)", (nom, email))
                conn.commit()
                st.success("Client ajouté avec succès.")

# Voir les réservations
elif menu == "Voir Réservations":
    st.subheader("📅 Réservations")
    cursor.execute("""
    
    SELECT R.Id_Reservation, C.Nom_complet, R.Date_arrivee, R.Date_depart
    FROM Reservation R
    JOIN Client C ON R.idClient = C.idClient
    """)
    rows = cursor.fetchall()
    if rows:
        st.table(rows)
    else:
        st.warning("Aucune réservation trouvée.")

# Rechercher et réserver une chambre
elif menu == "Chambres Disponibles":
    st.subheader("🛏️ Recherche de Chambres Disponibles")
    with st.form("form_search"):
        date_arr = st.date_input("Date d'arrivée", min_value=date.today())
        date_dep = st.date_input("Date de départ", min_value=date.today())
        submitted = st.form_submit_button("Chercher")

    if submitted:
        if date_dep <= date_arr:
            st.error("❌ La date de départ doit être après la date d'arrivée.")
        else:
            query = """
            SELECT * FROM Chambre
            WHERE idChambre NOT IN (
                SELECT Id_Chambre FROM Concerner
                JOIN Reservation ON Concerner.Id_Reservation = Reservation.Id_Reservation
                WHERE Reservation.Date_arrivee <= ? AND Reservation.Date_depart >= ?
            )
            """
            cursor.execute(query, (date_dep.isoformat(), date_arr.isoformat()))
            chambres = cursor.fetchall()

            if chambres:
                st.success(f"{len(chambres)} chambre(s) disponible(s).")
                st.table(chambres)

                options = {f"Chambre {c[0]} - {c[1]}": c[0] for c in chambres}
                selected_label = st.selectbox("Choisissez une chambre :", list(options.keys()))
                selected_id = options[selected_label]

                # Liste des clients pour sélection
                cursor.execute("SELECT idClient, Nom_complet FROM Client")
                clients = cursor.fetchall()
                if clients:
                    client_options = {f"{c[0]} - {c[1]}": c[0] for c in clients}
                    client_label = st.selectbox("Choisissez un client :", list(client_options.keys()))
                    id_client = client_options[client_label]

                    if st.button("Réserver cette chambre"):
                        try:
                            cursor.execute("""
                                INSERT INTO Reservation (idClient, Date_arrivee, Date_depart)
                                VALUES (?, ?, ?)
                            """, (id_client, date_arr.isoformat(), date_dep.isoformat()))
                            conn.commit()

                            id_reservation = cursor.lastrowid

                            cursor.execute("""
                                INSERT INTO Concerner (Id_Reservation, Id_Chambre)
                                VALUES (?, ?)
                            """, (id_reservation, selected_id))
                            conn.commit()

                            st.success(f"✅ Réservation #{id_reservation} effectuée pour le client {id_client}.")
                        except Exception as e:
                            st.error(f"❌ Erreur : {e}")
                else:
                    st.warning("Aucun client enregistré. Veuillez d’abord ajouter un client.")
            else:
                st.warning("Aucune chambre disponible à ces dates.")

# Fermer la connexion
conn.close()
