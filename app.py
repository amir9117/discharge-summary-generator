from groq import Groq
import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv(".env")
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# Load patient data from the JSON file
def load_patient_data(filepath="patients_data.json"):
    with open(filepath, "r") as file:
        return json.load(file)

# Fetch patient by name and ID
def get_patient_by_id_and_name(patient_id, name, data):
    for patient in data:
        if patient["id"].strip() == patient_id.strip() and patient["name"].strip().lower() == name.strip().lower():
            return patient
    return None

# Load all patient data
data = load_patient_data()




st.title("Discharge Summary Generator")

patient_name = st.text_input("Enter Patient's Name")
patient_id = st.text_input("Enter Patient's ID")

if st.button("Generate Summary"):
    if not patient_name or not patient_id:
        st.warning("Please enter both patient name and ID.")
    else:
        patient_data = get_patient_by_id_and_name(patient_id, patient_name, data)
        
        patient_info = f"""
        -  **Name:** {patient_data['name']}
        -  **Patient ID:** {patient_data['id']}
        -  **Age:** {patient_data['age']}
        -  **Gender:** {patient_data['gender']}
        -  **Admission Date:** {patient_data['admission_date']}
        -  **Discharge Date:** {patient_data['discharge_date']}
        """


        if not patient_data:
            st.error("Patient not found.")
        else:
            st.success("Patient found. Generating summary...")

            # Format the prompt
            prompt = f"""
            You are a professional medical documentation assistant. Your task is to generate a formal hospital discharge summary based solely on the following structured patient data.

            Do not include anything outside the data provided.

            Output the summary in proper paragraph format with appropriate medical tone and coherence.

            Patient Data:
            {patient_data}
            """

            # Connect to Groq
            client = Groq()

            # Create the completion call
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            # Display the streamed output
            summary = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                summary += content
                

            st.markdown("###  Patient Information")
            st.markdown(patient_info)

            st.subheader("Discharge Summary")
            st.text_area("Full Summary", summary, height=300)




