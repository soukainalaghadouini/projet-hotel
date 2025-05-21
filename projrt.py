import mysql.connector
from mysql.connector import Error

try:
    
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="b.laghadouini@75",  
        database="hoteldb"          
    )

    if mysql_conn.is_connected():
        print("connecte")
        
       
        cursor = mysql_conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        print(" HotelDB: existe")
        for table in tables:
            print("-", table[0])

except Error as e:
    print("erreur", e)

finally:
    if 'mysql_conn' in locals() and mysql_conn.is_connected():
        cursor.close()
        mysql_conn.close()
        print("jkj")

