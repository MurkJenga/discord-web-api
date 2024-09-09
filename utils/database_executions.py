import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()

def execute_query(query, action, log, args = None):
    dbconfig = {
        "user": os.getenv('DATABASE_USER'), 
        "password": os.getenv('DATABASE_PASS'), 
        "host": os.getenv('HOST'), 
        "database": os.getenv('DATABASE_NAME'), 
    }
    
    cnxpool = pooling.MySQLConnectionPool(pool_name="mypool",
                                        pool_size=5,
                                        **dbconfig)
        
    cnx = cnxpool.get_connection() 
    cursor = cnx.cursor()

    try:
        if action != 'select':
            cursor.execute(query, args) 
            cnx.commit()
        else:
            cursor.execute(query, args) 
    except Exception as e:
        print(e)

    cursor.close()
    cnx.close()

    print(log) 