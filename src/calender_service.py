from ics import Calendar, Event
from datetime import datetime, timedelta
import os


def create_calendar_invite(
    appointment_id,
    patient_name,
    doctor_name,
    appointment_date,
    appointment_time
):
    """
    Generates an .ics calendar invite file.
    """

    start_time = datetime.strptime(
        f"{appointment_date} {appointment_time}",
        "%Y-%m-%d %H:%M:%S"
    )

    end_time = start_time + timedelta(minutes=30)

    calendar = Calendar()

    event = Event()
    event.name = f"Appointment with {doctor_name}"
    event.begin = start_time
    event.end = end_time

    event.description = (
        f"Patient: {patient_name}\n"
        f"Doctor: {doctor_name}"
    )

    calendar.events.add(event)

    os.makedirs("calendar_invites", exist_ok=True)

    file_path = (
        f"calendar_invites/"
        f"appointment_{appointment_id}.ics"
    )

    with open(file_path, "w") as f:
        f.writelines(calendar)

    return file_path