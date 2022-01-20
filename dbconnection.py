import mysql.connector
from mysql.connector import Error

# Connect to the database

def create_server_connection(host_name, user_name, user_password):
    try:
        connection = mysql.connector.connect(host=host_name,
                                             user=user_name,
                                             passwd=user_password)
        print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print("Error while connecting to MySQL DB", e)
        return None
    
# test connection to SQL server
create_server_connection("104.188.187.36", "disbot", "sv_cheats 1")