import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

def get_db_connection():
    conn = pymysql.connect(
        host= db_host,
        user= db_user,
        password= db_password,
        database= db_name
    )
    return conn