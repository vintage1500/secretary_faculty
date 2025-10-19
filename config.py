from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
PROVIDER_TOKEN = ""
ADMINS = ''

DB_NAME = os.getenv('DB_NAME', 'secretary_faculty_db')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5433')
DB_USER = os.getenv('DB_USER', 'postgres')


