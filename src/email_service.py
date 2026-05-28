
 
import yagmail
import os
from dotenv import load_dotenv
 
load_dotenv()
 
 
def send_booking_email(
    patient_email,
    patient_name,
    doctor_name,
    appointment_date,
    appointment_time,
    attachment_path
):
    print("EMAIL_USER =", os.getenv("EMAIL_USER"))
    print("EMAIL_PASSWORD =", os.getenv("EMAIL_PASSWORD"))
 
    yag = yagmail.SMTP(
        user=os.getenv("EMAIL_USER"),
        password=os.getenv("EMAIL_PASSWORD")
    )
 
    subject = "Appointment Confirmation"
 
    body = f"""
Hello {patient_name},
 
Your appointment has been confirmed.
 
Doctor: {doctor_name}
Date: {appointment_date}
Time: {appointment_time}
 
The attached calendar invite can be added to your calendar.
 
Thank you.
"""
 
    yag.send(
        to=patient_email,
        subject=subject,
        contents=body,
        attachments=attachment_path
    )
 
    return True
 