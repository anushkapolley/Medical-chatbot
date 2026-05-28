# # # # # from langchain_groq import ChatGroq
# # # # # from datetime import datetime
# # # # # import json

# # # # # llm = ChatGroq(
# # # # #     model_name="llama-3.1-8b-instant"
# # # # # )

# # # # # def detect_intent(user_msg):

# # # # #     prompt=f"""
# # # # # Classify the message into one category only:

# # # # # medical
# # # # # appointment
# # # # # cancel
# # # # # reschedule

# # # # # Message:
# # # # # {user_msg}

# # # # # Return only category.
# # # # # """

# # # # #     response=llm.invoke(prompt)

# # # # #     return response.content.strip().lower()


# # # # # def extract_appointment_info(user_msg):

# # # # #     prompt=f"""
# # # # # Extract details from:

# # # # # {user_msg}

# # # # # Return JSON only:

# # # # # {{
# # # # # "speciality":"",
# # # # # "date":"",
# # # # # "time":""
# # # # # }}
# # # # # """

# # # # #     result=llm.invoke(prompt)

# # # # #     try:
# # # # #         return json.loads(result.content)

# # # # #     except:
# # # # #         return None
# # # # from langchain_groq import ChatGroq
# # # # from datetime import datetime
# # # # import json
# # # # import re

# # # # llm = ChatGroq(
# # # #     model_name="llama-3.1-8b-instant"
# # # # )


# # # # # =========================
# # # # # DETECT USER INTENT
# # # # # =========================
# # # # def detect_intent(user_msg):

# # # #     prompt = f"""
# # # # Classify the message into one category only:

# # # # medical
# # # # appointment
# # # # cancel
# # # # reschedule

# # # # Message:
# # # # {user_msg}

# # # # Return only category.
# # # # """

# # # #     response = llm.invoke(prompt)

# # # #     return response.content.strip().lower()


# # # # # =========================
# # # # # EXTRACT APPOINTMENT INFO
# # # # # =========================
# # # # def extract_appointment_info(user_msg):

# # # #     text = user_msg.lower()

# # # #     # -------------------------
# # # #     # SPECIALITY EXTRACTION
# # # #     # -------------------------
# # # #     speciality = None

# # # #     specialities = [
# # # #         "cardiologist",
# # # #         "dermatologist",
# # # #         "neurologist",
# # # #         "orthopedic",
# # # #         "pediatrician",
# # # #         "general"
# # # #     ]

# # # #     for s in specialities:
# # # #         if s in text:
# # # #             speciality = s
# # # #             break

# # # #     # -------------------------
# # # #     # DATE EXTRACTION
# # # #     # Supports:
# # # #     # 29-05-2026
# # # #     # -------------------------
# # # #     date = None

# # # #     date_match = re.search(
# # # #         r"(\d{2})-(\d{2})-(\d{4})",
# # # #         text
# # # #     )

# # # #     if date_match:

# # # #         raw_date = date_match.group()

# # # #         parsed_date = datetime.strptime(
# # # #             raw_date,
# # # #             "%d-%m-%Y"
# # # #         )

# # # #         date = parsed_date.strftime("%Y-%m-%d")

# # # #     # -------------------------
# # # #     # TIME EXTRACTION
# # # #     # Supports:
# # # #     # 14:30
# # # #     # 10:30
# # # #     # 5 PM
# # # #     # 10 AM
# # # #     # -------------------------
# # # #     time = None

# # # #     # HH:MM format
# # # #     time_match = re.search(
# # # #         r"(\d{1,2}):(\d{2})",
# # # #         text
# # # #     )

# # # #     if time_match:

# # # #         hour = int(time_match.group(1))
# # # #         minute = int(time_match.group(2))

# # # #         time = f"{hour:02d}:{minute:02d}:00"

# # # #     else:

# # # #         # AM/PM format
# # # #         time_match = re.search(
# # # #             r"(\d{1,2})\s*(am|pm)",
# # # #             text
# # # #         )

# # # #         if time_match:

# # # #             hour = int(time_match.group(1))
# # # #             meridian = time_match.group(2)

# # # #             if meridian == "pm" and hour != 12:
# # # #                 hour += 12

# # # #             time = f"{hour:02d}:00:00"

# # # #     # -------------------------
# # # #     # VALIDATION
# # # #     # -------------------------
# # # #     if not speciality or not date or not time:
# # # #         return None

# # # #     return {
# # # #         "speciality": speciality,
# # # #         "date": date,
# # # #         "time": time
# # # #     }
# # # from langchain_groq import ChatGroq
# # # from datetime import datetime
# # # import json
# # # import re

# # # llm = ChatGroq(
# # #     model_name="llama-3.1-8b-instant"
# # # )

# # # # -----------------------------
# # # # Detect Intent
# # # # -----------------------------
# # # def detect_intent(user_msg):

# # #     prompt = f"""
# # # Classify the message into ONE category only:

# # # medical
# # # appointment
# # # cancel
# # # reschedule

# # # Message:
# # # {user_msg}

# # # Return only one word.
# # # """

# # #     response = llm.invoke(prompt)

# # #     return response.content.strip().lower()


# # # # -----------------------------
# # # # Extract Appointment Details
# # # # -----------------------------
# # # def extract_appointment_info(user_msg):

# # #     prompt = f"""
# # # Extract appointment details from the user message.

# # # Message:
# # # {user_msg}

# # # Rules:
# # # - Convert date into YYYY-MM-DD format
# # # - Convert time into HH:MM format
# # # - Fix spelling mistakes in speciality names
# # # - Return ONLY valid JSON
# # # - No explanation
# # # - No markdown

# # # Example:

# # # {{
# # #     "speciality":"Pediatrician",
# # #     "date":"2026-05-29",
# # #     "time":"14:30"
# # # }}
# # # """

# # #     response = llm.invoke(prompt)

# # #     content = response.content.strip()

# # #     print("RAW LLM RESPONSE:", content)

# # #     # remove markdown if present
# # #     content = content.replace("```json", "")
# # #     content = content.replace("```", "")
# # #     content = content.strip()

# # #     try:
# # #         details = json.loads(content)

# # #         speciality = details.get("speciality")
# # #         date = details.get("date")
# # #         time = details.get("time")

# # #         # validate fields
# # #         if not speciality or not date or not time:
# # #             return None

# # #         return details

# # #     except Exception as e:
# # #         print("JSON ERROR:", e)
# # #         return None
# # from langchain_groq import ChatGroq
# # from datetime import datetime
# # import json
# # import re

# # llm = ChatGroq(
# #     model_name="llama-3.1-8b-instant"
# # )

# # # =========================
# # # Detect Intent
# # # =========================
# # def detect_intent(user_msg):

# #     msg = user_msg.lower()

# #     if "book" in msg or "appointment" in msg:
# #         return "appointment"

# #     elif "cancel" in msg:
# #         return "cancel"

# #     elif "reschedule" in msg:
# #         return "reschedule"

# #     else:
# #         return "medical"


# # # =========================
# # # Extract Appointment Info
# # # =========================
# # def extract_appointment_info(user_msg):

# #     msg = user_msg.lower().strip()

# #     speciality = None

# #     specialities = [
# #         "cardiologist",
# #         "dermatologist",
# #         "neurologist",
# #         "orthopedic",
# #         "pediatrician"
# #     ]

# #     for s in specialities:
# #         if s in msg:
# #             speciality = s
# #             break

# #     # =========================
# #     # DATE
# #     # Supports:
# #     # 29-05-2026
# #     # 29/05/2026
# #     # =========================

# #     date = None

# #     date_match = re.search(r"(\d{2})[-/](\d{2})[-/](\d{4})", msg)

# #     if date_match:

# #         day = date_match.group(1)
# #         month = date_match.group(2)
# #         year = date_match.group(3)

# #         date = f"{year}-{month}-{day}"

# #     # =========================
# #     # TIME
# #     # Supports:
# #     # 10:30
# #     # 5 PM
# #     # 5PM
# #     # =========================

# #     time = None

# #     # 10:30 format
# #     time_match = re.search(r"\d{1,2}:\d{2}", msg)

# #     if time_match:

# #         time = time_match.group()

# #     else:

# #         # 5 PM format
# #         am_pm_match = re.search(r"(\d{1,2})\s?(am|pm)", msg)

# #         if am_pm_match:

# #             hour = int(am_pm_match.group(1))
# #             period = am_pm_match.group(2)

# #             if period == "pm" and hour != 12:
# #                 hour += 12

# #             if period == "am" and hour == 12:
# #                 hour = 0

# #             time = f"{hour:02d}:00"

# #     return {
# #         "speciality": speciality,
# #         "date": date,
# #         "time": time
# #     }
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

#     if any(word in msg for word in ["book", "appointment"]):
#         return "appointment"

#     elif "cancel" in msg:
#         return "cancel"

#     elif "reschedule" in msg:
#         return "reschedule"

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
#         "pediatrician"
#     ]

#     for s in specialities:
#         if s in msg:
#             speciality = s
#             break

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

from langchain_groq import ChatGroq
import re
from datetime import datetime

llm = ChatGroq(
    model_name="llama-3.1-8b-instant"
)

# =========================
# DETECT INTENT
# =========================
def detect_intent(user_msg):

    msg = user_msg.lower()

    # ✅ FIX: Check specific intents BEFORE generic "appointment" keyword
    # "reschedule appointment" and "cancel appointment" were matching "appointment" first
    if "reschedule" in msg:
        return "reschedule"

    elif "cancel" in msg:
        return "cancel"

    elif any(word in msg for word in ["book", "appointment"]):
        return "appointment"

    return "medical"


# =========================
# EXTRACT DETAILS
# =========================
def extract_appointment_info(user_msg):

    msg = user_msg.lower().strip()

    # -------------------------
    # SPECIALITY
    # -------------------------
    speciality = None

    specialities = [
        "cardiologist",
        "dermatologist",
        "neurologist",
        "orthopedic",
        "pediatrician",
        "gynecologist",
        "ent specialist"
    ]

    for s in specialities:
        if s in msg:
            speciality = s
            break

    # ✅ FIX: Convert to Title Case to match DB values
    # DB stores "Cardiologist" but extraction returns "cardiologist"
    if speciality:
        speciality = speciality.title()

    # -------------------------
    # DATE
    # -------------------------
    date = None

    date_match = re.search(
        r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})',
        msg
    )

    if date_match:

        day = int(date_match.group(1))
        month = int(date_match.group(2))
        year = int(date_match.group(3))

        try:
            formatted_date = datetime(
                year,
                month,
                day
            )

            date = formatted_date.strftime("%Y-%m-%d")

        except:
            date = None

    # -------------------------
    # TIME
    # -------------------------
    time = None

    # 10:30 format
    time_match = re.search(
        r'(\d{1,2}):(\d{2})',
        msg
    )

    if time_match:

        hour = int(time_match.group(1))
        minute = int(time_match.group(2))

        time = f"{hour:02d}:{minute:02d}:00"

    else:

        # 5 PM format
        am_pm_match = re.search(
            r'(\d{1,2})\s?(am|pm)',
            msg
        )

        if am_pm_match:

            hour = int(am_pm_match.group(1))
            period = am_pm_match.group(2)

            if period == "pm" and hour != 12:
                hour += 12

            if period == "am" and hour == 12:
                hour = 0

            time = f"{hour:02d}:00:00"

    print("EXTRACTED:")
    print({
        "speciality": speciality,
        "date": date,
        "time": time
    })

    return {
        "speciality": speciality,
        "date": date,
        "time": time
    }