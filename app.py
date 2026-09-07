from flask import Flask, render_template, jsonify, request, session
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os
import re
 
load_dotenv()
 
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Missing API keys! Set PINECONE_API_KEY and OPENAI_API_KEY in environment variables.")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
 
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medical-chatbot-secret-key")
 
embeddings = download_embeddings()
 
index_name = "medicalchatbot"
 
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
 
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
 
chatModel = ChatOpenAI(model="gpt-4o-mini")
 
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)
 
question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
 
from src.agent import detect_intent, extract_appointment_info
from src.appointment import (
    get_doctors_by_speciality,
    get_available_slots,
    book_appointment,
    cancel_appointment,
    reschedule_appointment
)
 
 
# =========================
# HELPER: Extract ID, date, time from message
# =========================
def extract_id(msg):
    match = re.search(r'\b(\d+)\b', msg)
    return int(match.group(1)) if match else None
 
def extract_date_time(msg):
    date = None
    time = None
 
    date_match = re.search(r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})', msg)
    if date_match:
        from datetime import datetime
        try:
            date = datetime(
                int(date_match.group(3)),
                int(date_match.group(2)),
                int(date_match.group(1))
            ).strftime("%Y-%m-%d")
        except:
            date = None
 
    time_match = re.search(r'(\d{1,2}):(\d{2})', msg)
    if time_match:
        time = f"{int(time_match.group(1)):02d}:{time_match.group(2)}:00"
    else:
        am_pm = re.search(r'(\d{1,2})\s?(am|pm)', msg.lower())
        if am_pm:
            hour = int(am_pm.group(1))
            period = am_pm.group(2)
            if period == "pm" and hour != 12:
                hour += 12
            if period == "am" and hour == 12:
                hour = 0
            time = f"{hour:02d}:00:00"
 
    return date, time
 
 
@app.route("/health")
def health():
    return "Endpoint hit successfully"
 
 
@app.route("/")
def index():
    return render_template('chat.html')
 
 
@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
 
    intent = detect_intent(msg)
    print("Intent:", intent)
 
    # Override intent if we're mid-flow in any pending session
    if "pending_appointment" in session:
        intent = "appointment"
    elif "pending_reschedule" in session:
        intent = "reschedule"
    elif "pending_cancel" in session:
        intent = "cancel"
 
    # =========================
    # APPOINTMENT BOOKING
    # =========================
    if intent == "appointment":
 
        pending = session.get("pending_appointment", {})
        new_details = extract_appointment_info(msg)
 
        if new_details.get("speciality"):
            pending["speciality"] = new_details["speciality"].title()
        if new_details.get("date"):
            pending["date"] = new_details["date"]
        if new_details.get("time"):
            pending["time"] = new_details["time"]
 
        session["pending_appointment"] = pending
        session.modified = True
 
        speciality = pending.get("speciality")
        date = pending.get("date")
        time = pending.get("time")
 
        if not speciality:
            return "Please mention the doctor speciality (e.g. Cardiologist, Dermatologist)."
        if not date:
            return "Please provide the appointment date (e.g. 28/05/2026)."
        if not time:
            return "Please provide the appointment time (e.g. 14:00 or 2 PM)."
        # ADD these 3 lines instead:
        from src.appointment import find_doctor_for_slot
        doctor = find_doctor_for_slot(speciality, date, time)
        if not doctor:
            session.pop("pending_appointment", None)
            return f"Sorry, no {speciality} doctor has a slot on {date} at {time}."
     
 
        result = book_appointment(
            patient_name="Anushka",
            patient_email="user@gmail.com",
            doctor_id=doctor["id"],
            appointment_date=date,
            appointment_time=time
        )
 
        session.pop("pending_appointment", None)
 
        if result["success"]:
            return (
                f"✅ Appointment booked successfully!\n\n"
                f"👨‍⚕️ Doctor: {doctor['name']}\n"
                f"📅 Date: {date}\n"
                f"⏰ Time: {time}\n\n"
                f"📧 Confirmation email sent."
            )
 
        return f"❌ {result['message']}"
 
    # =========================
    # CANCEL APPOINTMENT
    # =========================
    elif intent == "cancel":
 
        pending = session.get("pending_cancel", {})
 
        # Try to extract appointment ID from message
        extracted_id = extract_id(msg)
        if extracted_id:
            pending["appointment_id"] = extracted_id
 
        session["pending_cancel"] = pending
        session.modified = True
 
        appointment_id = pending.get("appointment_id")
 
        if not appointment_id:
            return "Please provide your appointment ID to cancel (e.g. 'cancel appointment 3')."
 
        # Confirm before cancelling
        if not pending.get("confirmed"):
            pending["confirmed"] = True
            session["pending_cancel"] = pending
            session.modified = True
            return f"Are you sure you want to cancel appointment ID {appointment_id}? Reply 'yes' to confirm."
 
        # Check for confirmation
        if msg.strip().lower() in ["yes", "confirm", "y"]:
            result = cancel_appointment(appointment_id)
            session.pop("pending_cancel", None)
            return f"✅ Appointment {appointment_id} has been cancelled successfully."
        else:
            session.pop("pending_cancel", None)
            return "❌ Cancellation aborted."
 
    # =========================
    # RESCHEDULE APPOINTMENT
    # =========================
    elif intent == "reschedule":
 
        pending = session.get("pending_reschedule", {})
 
        # Extract appointment ID
        extracted_id = extract_id(msg)
        if extracted_id and not pending.get("appointment_id"):
            pending["appointment_id"] = extracted_id
 
        # Extract new date and time
        new_date, new_time = extract_date_time(msg)
        if new_date:
            pending["new_date"] = new_date
        if new_time:
            pending["new_time"] = new_time
 
        session["pending_reschedule"] = pending
        session.modified = True
 
        print("Reschedule Pending:", pending)
 
        appointment_id = pending.get("appointment_id")
        new_date = pending.get("new_date")
        new_time = pending.get("new_time")
 
        if not appointment_id:
            return "Please provide your appointment ID to reschedule (e.g. 'reschedule appointment 3')."
        if not new_date:
            return f"Please provide the new date for appointment {appointment_id} (e.g. 01/06/2026)."
        if not new_time:
            return f"Please provide the new time for appointment {appointment_id} (e.g. 11:00 or 2 PM)."
 
        # All info collected — proceed
        result = reschedule_appointment(
            appointment_id=appointment_id,
            new_date=new_date,
            new_time=new_time
        )
 
        session.pop("pending_reschedule", None)
 
        if "successfully" in result["message"].lower():
            return (
                f"✅ Appointment {appointment_id} rescheduled successfully!\n\n"
                f"📅 New Date: {new_date}\n"
                f"⏰ New Time: {new_time}"
            )
 
        return f"❌ {result['message']}"
 
    # =========================
    # MEDICAL QUERY (RAG)
    # =========================
    else:
        response = rag_chain.invoke({"input": msg})
        return response["answer"]
 
 
# =========================
# REST API ROUTES
# =========================
 
@app.route("/doctors/<speciality>", methods=["GET"])
def doctors(speciality):
    try:
        data = get_doctors_by_speciality(speciality)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
 
@app.route("/availability/<int:doctor_id>", methods=["GET"])
def availability(doctor_id):
    data = get_available_slots(doctor_id)
    return jsonify(data)
 
 
@app.route("/book", methods=["POST"])
def book():
    data = request.json
    result = book_appointment(
        patient_name=data["patient_name"],
        patient_email=data["patient_email"],
        doctor_id=data["doctor_id"],
        appointment_date=data["appointment_date"],
        appointment_time=data["appointment_time"]
    )
    return jsonify(result)
 
 
@app.route("/cancel/<int:appointment_id>", methods=["PUT"])
def cancel(appointment_id):
    result = cancel_appointment(appointment_id)
    return jsonify(result)
 
 
@app.route("/reschedule", methods=["PUT"])
def reschedule():
    data = request.json
    result = reschedule_appointment(
        appointment_id=data["appointment_id"],
        new_date=data["new_date"],
        new_time=data["new_time"]
    )
    return jsonify(result)
 
 
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(app.url_map)
    app.run(host="0.0.0.0", port=port, debug=True)
