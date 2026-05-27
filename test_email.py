# test_email.py

from src.email_service import send_booking_email

send_booking_email(
    patient_email="your_email@gmail.com",
    patient_name="Anushka",
    doctor_name="Dr Amit Sharma",
    appointment_date="2026-06-03",
    appointment_time="11:00:00",
    attachment_path="calendar_invites/appointment_1.ics"
)

print("Email Sent")