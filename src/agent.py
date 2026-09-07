
 
# from langchain_groq import ChatGroq
# import re
# from datetime import datetime
 
# llm = ChatGroq(
#     model_name="llama-3.1-8b-instant"
# )
 
# # =========================
# # DETECT INTENT
# # =========================
# def detect_intent(user_msg):
 
#     msg = user_msg.lower()
 
#     # ✅ FIX: Check specific intents BEFORE generic "appointment" keyword
#     # "reschedule appointment" and "cancel appointment" were matching "appointment" first
#     if "reschedule" in msg:
#         return "reschedule"
 
#     elif "cancel" in msg:
#         return "cancel"
 
#     elif any(word in msg for word in ["book", "appointment"]):
#         return "appointment"
 
#     return "medical"
 
 
# # =========================
# # EXTRACT DETAILS
# # =========================
# def extract_appointment_info(user_msg):
 
#     msg = user_msg.lower().strip()
 
#     # -------------------------
#     # SPECIALITY
#     # -------------------------
#     speciality = None
 
#     specialities = [
#         "cardiologist",
#         "dermatologist",
#         "neurologist",
#         "orthopedic",
#         "pediatrician",
#         "gynecologist",
#         "ent specialist"
#     ]
 
#     for s in specialities:
#         if s in msg:
#             speciality = s
#             break
 
#     # ✅ FIX: Convert to Title Case to match DB values
#     # DB stores "Cardiologist" but extraction returns "cardiologist"
#     if speciality:
#         speciality = speciality.title()
 
#     # -------------------------
#     # DATE
#     # -------------------------
#     date = None
 
#     date_match = re.search(
#         r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})',
#         msg
#     )
 
#     if date_match:
 
#         day = int(date_match.group(1))
#         month = int(date_match.group(2))
#         year = int(date_match.group(3))
 
#         try:
#             formatted_date = datetime(
#                 year,
#                 month,
#                 day
#             )
 
#             date = formatted_date.strftime("%Y-%m-%d")
 
#         except:
#             date = None
 
#     # -------------------------
#     # TIME
#     # -------------------------
#     time = None
 
#     # 10:30 format
#     time_match = re.search(
#         r'(\d{1,2}):(\d{2})',
#         msg
#     )
 
#     if time_match:
 
#         hour = int(time_match.group(1))
#         minute = int(time_match.group(2))
 
#         time = f"{hour:02d}:{minute:02d}:00"
 
#     else:
 
#         # 5 PM format
#         am_pm_match = re.search(
#             r'(\d{1,2})\s?(am|pm)',
#             msg
#         )
 
#         if am_pm_match:
 
#             hour = int(am_pm_match.group(1))
#             period = am_pm_match.group(2)
 
#             if period == "pm" and hour != 12:
#                 hour += 12
 
#             if period == "am" and hour == 12:
#                 hour = 0
 
#             time = f"{hour:02d}:00:00"
 
#     print("EXTRACTED:")
#     print({
#         "speciality": speciality,
#         "date": date,
#         "time": time
#     })
 
#     return {
#         "speciality": speciality,
#         "date": date,
#         "time": time
#     }
 
import re
from datetime import datetime

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")


# ─────────────────────────────────────────────────────────────
# SPECIALITY LIST  (single source of truth used by both functions)
# ─────────────────────────────────────────────────────────────

SPECIALITIES = [
    "cardiologist",
    "dermatologist",
    "neurologist",
    "orthopedic",
    "pediatrician",
    "gynecologist",
    "ent specialist",
    "general physician",
    "psychiatrist",
    "urologist",
    "ophthalmologist",
]


# ─────────────────────────────────────────────────────────────
# INTENT DETECTION
# ─────────────────────────────────────────────────────────────

def detect_intent(user_msg):
    msg = user_msg.lower().strip()

    # Reschedule and cancel MUST be checked before "appointment"
    # because phrases like "reschedule appointment" contain the word
    # "appointment" which would match the booking branch first.
    if any(word in msg for word in [
        "reschedule", "change appointment",
        "move appointment", "shift appointment"
    ]):
        return "reschedule"

    if any(word in msg for word in [
        "cancel", "delete appointment", "remove appointment"
    ]):
        return "cancel"

    # Explicit booking keywords
    if any(word in msg for word in [
        "book", "appointment", "slot",
        "schedule an", "fix an appointment",
        "set up an appointment", "arrange an appointment",
        "i need a doctor", "see a doctor",
        "visit a doctor", "book a doctor"
    ]):
        return "appointment"

    # FIX: If user just says the speciality (e.g. "Cardiologist on 30/05/2026
    # at 10:00") without a booking keyword, still treat as appointment.
    if any(s in msg for s in SPECIALITIES):
        return "appointment"

    return "medical"


# ─────────────────────────────────────────────────────────────
# EXTRACT APPOINTMENT DETAILS
# ─────────────────────────────────────────────────────────────

def extract_appointment_info(user_msg):
    msg = user_msg.lower().strip()

    # ── SPECIALITY ──────────────────────────────────────────
    speciality = None
    for s in SPECIALITIES:
        if s in msg:
            speciality = s.title()   # e.g. "cardiologist" -> "Cardiologist"
            break

    # ── DATE ────────────────────────────────────────────────
    # FIX: previously only handled DD/MM/YYYY — missed ISO format entirely.
    # Now handles BOTH formats:
    #   • YYYY-MM-DD  →  e.g. 2026-05-30   (ISO, what users often type)
    #   • DD/MM/YYYY  →  e.g. 29/05/2026   (or with - or . separators)

    date = None

    # Try ISO format first: YYYY-MM-DD
    iso_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', msg)
    if iso_match:
        try:
            date = datetime(
                int(iso_match.group(1)),
                int(iso_match.group(2)),
                int(iso_match.group(3))
            ).strftime("%Y-%m-%d")
        except ValueError:
            date = None

    # Fall back to DD/MM/YYYY (or DD-MM-YYYY, DD.MM.YYYY)
    if not date:
        dmy_match = re.search(r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})', msg)
        if dmy_match:
            try:
                date = datetime(
                    int(dmy_match.group(3)),
                    int(dmy_match.group(2)),
                    int(dmy_match.group(1))
                ).strftime("%Y-%m-%d")
            except ValueError:
                date = None

    # ── TIME ────────────────────────────────────────────────
    time = None

    # HH:MM format (e.g. 14:00, 09:30, 10:00)
    time_match = re.search(r'(\d{1,2}):(\d{2})', msg)
    if time_match:
        hour   = int(time_match.group(1))
        minute = int(time_match.group(2))
        time   = f"{hour:02d}:{minute:02d}:00"
    else:
        # H am/pm format (e.g. 2 PM, 9am, 11 AM)
        am_pm_match = re.search(r'(\d{1,2})\s*(am|pm)', msg)
        if am_pm_match:
            hour   = int(am_pm_match.group(1))
            period = am_pm_match.group(2)
            if period == "pm" and hour != 12:
                hour += 12
            if period == "am" and hour == 12:
                hour = 0
            time = f"{hour:02d}:00:00"

    print("[Agent] Extracted:", {"speciality": speciality, "date": date, "time": time})

    return {
        "speciality": speciality,
        "date": date,
        "time": time
    }
