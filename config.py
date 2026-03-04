import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORTAL_URL = os.getenv('PORTAL_URL', 'https://portal.cardiofocus.com')
    USERNAME = os.getenv('USERNAME', '')
    PASSWORD = os.getenv('PASSWORD', '')
    
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://portal.cardiofocus.com/api')
    API_TOKEN = os.getenv('API_TOKEN', '')
    
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', '')
