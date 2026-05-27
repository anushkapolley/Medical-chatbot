import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASSWORD")

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(email, password)

print("Login successful")
server.quit()