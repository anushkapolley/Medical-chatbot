# from src.database import get_connection
# from src.calender_service import create_calendar_invite
# from src.email_service import send_booking_email
# def get_doctors_by_speciality(speciality):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
 
#     query = """
#     SELECT *
#     FROM doctors
#     WHERE speciality=%s
#     """
 
#     cursor.execute(query, (speciality,))
#     doctors = cursor.fetchall()
 
#     cursor.close()
#     conn.close()
 
#     return doctors
 
# def get_available_slots(doctor_id):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
 
#     query = """
#     SELECT *
#     FROM availability
#     WHERE doctor_id=%s
#     AND available=TRUE
#     """
 
#     cursor.execute(query, (doctor_id,))
#     slots = cursor.fetchall()
 
#     cursor.close()
#     conn.close()
 
#     return slots
 
# def book_appointment(
#     patient_name,
#     patient_email,
#     doctor_id,
#     appointment_date,
#     appointment_time
# ):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
 
#     # Check slot availability
#     cursor.execute("""
#         SELECT * FROM availability
#         WHERE doctor_id=%s
#         AND slot_date=%s
#         AND slot_time=%s
#         AND available=TRUE
#     """, (doctor_id, appointment_date, appointment_time))
 
#     slot = cursor.fetchone()
 
#     if not slot:
#         cursor.close()
#         conn.close()
 
#         return {
#             "success": False,
#             "message": "Slot not available"
#         }
 
#     # Get doctor name
#     cursor.execute(
#         "SELECT name FROM doctors WHERE id=%s",
#         (doctor_id,)
#     )
 
#     doctor = cursor.fetchone()
#     doctor_name = doctor["name"]
 
#     # Insert appointment
#     cursor.execute("""
#         INSERT INTO appointments(
#             patient_name,
#             patient_email,
#             doctor_id,
#             appointment_date,
#             appointment_time,
#             status
#         )
#         VALUES(%s,%s,%s,%s,%s,%s)
#     """, (
#         patient_name,
#         patient_email,
#         doctor_id,
#         appointment_date,
#         appointment_time,
#         "Booked"
#     ))
 
#     appointment_id = cursor.lastrowid
 
#     # Mark slot unavailable
#     cursor.execute("""
#         UPDATE availability
#         SET available=FALSE
#         WHERE doctor_id=%s
#         AND slot_date=%s
#         AND slot_time=%s
#     """, (
#         doctor_id,
#         appointment_date,
#         appointment_time
#     ))
 
#     conn.commit()
 
#     # Create calendar invite
#     calendar_file = create_calendar_invite(
#         appointment_id=appointment_id,
#         patient_name=patient_name,
#         doctor_name=doctor_name,
#         appointment_date=str(appointment_date),
#         appointment_time=str(appointment_time)
#     )
 
#     # Send confirmation email
#     send_booking_email(
#         patient_email=patient_email,
#         patient_name=patient_name,
#         doctor_name=doctor_name,
#         appointment_date=appointment_date,
#         appointment_time=appointment_time,
#         attachment_path=calendar_file
#     )
 
#     cursor.close()
#     conn.close()
 
#     return {
#         "success": True,
#         "message": "Appointment booked successfully",
#         "appointment_id": appointment_id,
#         "calendar_file": calendar_file,
#         "email_sent": True
#     }
# def cancel_appointment(appointment_id):
#     conn = get_connection()
#     cursor = conn.cursor()
 
#     query = """
#     UPDATE appointments
#     SET status='Cancelled'
#     WHERE id=%s
#     """
 
#     cursor.execute(query, (appointment_id,))
#     conn.commit()
 
#     cursor.close()
#     conn.close()
 
#     return {
#         "message": "Appointment cancelled"
#     }
 
# def reschedule_appointment(
#     appointment_id,
#     new_date,
#     new_time
# ):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
 
#     # 1. Fetch current appointment
#     cursor.execute("""
#         SELECT *
#         FROM appointments
#         WHERE id = %s
#     """, (appointment_id,))
 
#     appointment = cursor.fetchone()
 
#     if not appointment:
#         cursor.close()
#         conn.close()
 
#         return {
#             "message": "Appointment not found"
#         }
 
#     doctor_id = appointment["doctor_id"]
 
#     old_date = appointment["appointment_date"]
#     old_time = appointment["appointment_time"]
 
#     cursor.execute("""
#         SELECT *
#         FROM availability
#         WHERE doctor_id = %s
#         AND slot_date = %s
#         AND slot_time = %s
#         AND available = TRUE
#     """,
#     (
#         doctor_id,
#         new_date,
#         new_time
#     ))
 
#     slot = cursor.fetchone()
 
#     if not slot:
#         cursor.close()
#         conn.close()
 
#         return {
#             "message": "Selected slot not available"
#         }
#     cursor.execute("""
#         UPDATE appointments
#         SET appointment_date = %s,
#             appointment_time = %s
#         WHERE id = %s
#     """,
#     (
#         new_date,
#         new_time,
#         appointment_id
#     ))
#     conn.commit()
 
#     cursor.close()
#     conn.close()
 
#     return {
#         "message": "Appointment rescheduled successfully"
#     }
from src.database import get_connection
from src.calender_service import create_calendar_invite
from src.email_service import send_booking_email
 
 
def get_doctors_by_speciality(speciality):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors WHERE speciality=%s", (speciality,))
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return doctors
 
 
def get_available_slots(doctor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM availability
        WHERE doctor_id=%s AND available=TRUE
    """, (doctor_id,))
    slots = cursor.fetchall()
    cursor.close()
    conn.close()
    return slots
 
def find_doctor_for_slot(speciality, appointment_date, appointment_time):
    doctors = get_doctors_by_speciality(speciality)
    for doctor in doctors:
        slots = get_available_slots(doctor["id"])
        for slot in slots:
            # ✅ Convert timedelta to string before comparing
            slot_time = slot["slot_time"]
            if hasattr(slot_time, 'seconds'):
                # timedelta object — convert to HH:MM:SS
                total_seconds = int(slot_time.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                slot_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            if (str(slot["slot_date"]) == str(appointment_date) and
                    str(slot_time) == str(appointment_time)):
                return doctor
    return None
 
 
def book_appointment(
    patient_name,
    patient_email,
    doctor_id,
    appointment_date,
    appointment_time
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
 
    # Check slot availability
    cursor.execute("""
        SELECT * FROM availability
        WHERE doctor_id=%s
        AND slot_date=%s
        AND slot_time=%s
        AND available=TRUE
    """, (doctor_id, appointment_date, appointment_time))
 
    slot = cursor.fetchone()
 
    if not slot:
        cursor.close()
        conn.close()
        return {
            "success": False,
            "message": "Slot not available"
        }
 
    # Get doctor name
    cursor.execute("SELECT name FROM doctors WHERE id=%s", (doctor_id,))
    doctor = cursor.fetchone()
    doctor_name = doctor["name"]
 
    # Insert appointment
    cursor.execute("""
        INSERT INTO appointments(
            patient_name, patient_email, doctor_id,
            appointment_date, appointment_time, status
        ) VALUES(%s,%s,%s,%s,%s,%s)
    """, (patient_name, patient_email, doctor_id, appointment_date, appointment_time, "Booked"))
 
    appointment_id = cursor.lastrowid
 
    # Mark slot unavailable
    cursor.execute("""
        UPDATE availability SET available=FALSE
        WHERE doctor_id=%s AND slot_date=%s AND slot_time=%s
    """, (doctor_id, appointment_date, appointment_time))
 
    conn.commit()
 
    # ✅ FIX: Email failure no longer crashes the booking
    calendar_file = None
    email_sent = False
    try:
        calendar_file = create_calendar_invite(
            appointment_id=appointment_id,
            patient_name=patient_name,
            doctor_name=doctor_name,
            appointment_date=str(appointment_date),
            appointment_time=str(appointment_time)
        )
        send_booking_email(
            patient_email=patient_email,
            patient_name=patient_name,
            doctor_name=doctor_name,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            attachment_path=calendar_file
        )
        email_sent = True
    except Exception as e:
        print(f"Email failed (booking still successful): {e}")
 
    cursor.close()
    conn.close()
 
    return {
        "success": True,
        "message": "Appointment booked successfully",
        "appointment_id": appointment_id,
        "calendar_file": calendar_file,
        "email_sent": email_sent
    }
 
 
def cancel_appointment(appointment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE appointments SET status='Cancelled' WHERE id=%s", (appointment_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Appointment cancelled"}
 
 
def reschedule_appointment(appointment_id, new_date, new_time):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
 
    cursor.execute("SELECT * FROM appointments WHERE id = %s", (appointment_id,))
    appointment = cursor.fetchone()
 
    if not appointment:
        cursor.close()
        conn.close()
        return {"message": "Appointment not found"}
 
    doctor_id = appointment["doctor_id"]
 
    cursor.execute("""
        SELECT * FROM availability
        WHERE doctor_id = %s AND slot_date = %s
        AND slot_time = %s AND available = TRUE
    """, (doctor_id, new_date, new_time))
 
    slot = cursor.fetchone()
 
    if not slot:
        cursor.close()
        conn.close()
        return {"message": "Selected slot not available"}
 
    # ✅ Free up old slot
    cursor.execute("""
        UPDATE availability SET available=TRUE
        WHERE doctor_id=%s AND slot_date=%s AND slot_time=%s
    """, (doctor_id, appointment["appointment_date"], appointment["appointment_time"]))
 
    # Update appointment
    cursor.execute("""
        UPDATE appointments
        SET appointment_date=%s, appointment_time=%s
        WHERE id=%s
    """, (new_date, new_time, appointment_id))
 
    # Mark new slot unavailable
    cursor.execute("""
        UPDATE availability SET available=FALSE
        WHERE doctor_id=%s AND slot_date=%s AND slot_time=%s
    """, (doctor_id, new_date, new_time))
 
    conn.commit()
    cursor.close()
    conn.close()
 
    return {"message": "Appointment rescheduled successfully"}
 