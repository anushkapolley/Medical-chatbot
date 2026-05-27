from src.calender_service import create_calendar_invite

file_path = create_calendar_invite(
    appointment_id=1,
    patient_name="Anushka Polley",
    doctor_name="Dr. Amit Sharma",
    appointment_date="2026-06-03",
    appointment_time="11:00:00"
)

print(file_path)