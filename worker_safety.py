import os
import pandas as pd
import streamlit as st

def load_data():
    if os.path.exists("worker_safety.csv"):
        df = pd.read_csv("worker_safety.csv")
    else:
        df = pd.DataFrame(columns=["Worker ID", "Department", "Job Role", "Shift",
                                    "PPE Compliance (%)", "Safety Training Status",
                                    "Fatigue Level", "Safety Observations",
                                    "Near Misses", "Previous Incidents", "Risk Level"])
    return df

def compute_risk_level(ppe, fatigue, near_misses, previous_incidents):
    score = 0

    if ppe < 70:
        score += 3
    elif ppe < 90:
        score += 1

    if fatigue == "Medium":
        score += 1
    elif fatigue == "High":
        score += 3

    if near_misses >= 3:
        score += 2
    elif near_misses >= 1:
        score += 1

    if previous_incidents >= 2:
        score += 2
    elif previous_incidents == 1:
        score += 1

    if score >= 7:
        return "Critical"
    elif score >= 5:
        return "High"
    elif score >= 2:
        return "Medium"
    else:
        return "Low"



def get_unsafe_condition_warnings(row):
    warnings = []

    if row["PPE Compliance (%)"] < 60:
        warnings.append("CRITICAL: PPE compliance very low.")
    elif row["PPE Compliance (%)"] < 80:
        warnings.append("WARNING: PPE compliance approaching unacceptable levels.")

    if row["Fatigue Level"] == "High":
        warnings.append("WARNING: High fatigue level.")

    if row["Near Misses"] >= 2:
        warnings.append("WARNING: Repeated near-misses recorded.")

    return warnings



def render_worker_safety_page():
    st.header("Worker Safety Monitoring")

    df = load_data()
    st.dataframe(df)

    st.subheader("Active Warnings")
    for index, row in df.iterrows():
        row_warnings = get_unsafe_condition_warnings(row)
        if row_warnings:
            st.warning(f"{row['Worker ID']}: " + " | ".join(row_warnings))

    st.subheader("Add New Worker Record")

    with st.form("add_worker_form", clear_on_submit=True):
        worker_id = st.text_input("Worker ID")
        department = st.selectbox("Department", ["Mining Operations", "Maintenance",
                                                    "Processing Plant", "Haulage", "Drilling", "Safety"])
        job_role = st.text_input("Job Role")
        shift = st.selectbox("Shift", ["Day", "Night"])
        ppe = st.slider("PPE Compliance (%)", 0, 100, 90)
        training = st.selectbox("Safety Training Status", ["Completed", "Pending", "Expired"])
        fatigue = st.selectbox("Fatigue Level", ["Low", "Medium", "High"])
        observations = st.text_area("Safety Observations", "No concerns noted")
        near_misses = st.number_input("Near Misses", min_value=0, value=0)
        previous_incidents = st.number_input("Previous Incidents", min_value=0, value=0)
        submitted = st.form_submit_button("Add Record")

    if submitted:
        if worker_id.strip() == "":
            st.error("Worker ID is required.")
        else:
            risk = compute_risk_level(ppe, fatigue, near_misses, previous_incidents)
            new_row = {
                "Worker ID": worker_id, "Department": department, "Job Role": job_role,
                "Shift": shift, "PPE Compliance (%)": ppe, "Safety Training Status": training,
                "Fatigue Level": fatigue, "Safety Observations": observations,
                "Near Misses": near_misses, "Previous Incidents": previous_incidents,
                "Risk Level": risk,
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv("worker_safety.csv", index=False)
            st.success(f"Record for {worker_id} added. Computed risk level: {risk}.")