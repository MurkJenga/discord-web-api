import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

dbconfig = {
    "user": os.getenv('DATABASE_USER'), 
    "password": os.getenv('DATABASE_PASS'), 
    "host": os.getenv('HOST'), 
    "database": os.getenv('DATABASE_NAME'), 
}

cnxpool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)

def execute_query(query, action, log, args=None):
    cnx = cnxpool.get_connection() 
    cursor = cnx.cursor()

    try: 
        if action != 'select': 
            cursor.execute(query, args) 
            cnx.commit() 
            logging.info(log) 
            return log
        else:
            cursor.execute(query, args) 
            result = cursor.fetchall()
            logging.info(log)
            return result
    except Exception as e:
        cnx.rollback()
        logging.error(f"Error executing query: {e}") 
    finally:
        cursor.close()
        cnx.close() 
