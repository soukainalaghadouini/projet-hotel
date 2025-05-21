import streamlit as st
import sqlite3

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

st.title("Système de Réservation d’Hôtel")

# 1. قائمة الحجوزات
if st.button("Voir les réservations"):
    cursor.execute("SELECT * FROM Reservation")
    rows = cursor.fetchall()
    st.write(rows)

# 2. قائمة العملاء
if st.button("Voir les clients"):
    cursor.execute("SELECT * FROM Client")
    rows = cursor.fetchall()
    st.write(rows)

# 3. عرض الغرف المتوفرة بين فترتين
with st.form("check_rooms"):
    date_start = st.date_input("Date d’arrivée")
    date_end = st.date_input("Date de départ")
    if st.form_submit_button("Chercher les chambres disponibles"):
        query = """
        SELECT * FROM Chambre WHERE Id_Chambre NOT IN (
            SELECT Id_Chambre FROM Concerner C
            JOIN Reservation R ON C.Id_Reservation = R.Id_Reservation
            WHERE R.Date_arrivee <= ? AND R.Date_depart >= ?
        );
        """
        cursor.execute(query, (date_end, date_start))
        st.write(cursor.fetchall())

# 4. إضافة عميل
with st.form("add_client"):
    name = st.text_input("Nom complet")
    email = st.text_input("Email")
    if st.form_submit_button("Ajouter Client"):
        cursor.execute("INSERT INTO Client (Nom_complet, Email) VALUES (?, ?)", (name, email))
        conn.commit()
        st.success("Client ajouté!")

# 5. إضافة حجز
# (يجب أن تبني الواجهة كاملة بعد إدخال العملاء والغرف)

conn.close()
