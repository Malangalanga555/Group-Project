import os
import pandas as pd
import streamlit as st

st.sidebar.image("MINE LOGO.png", width=400)

def load_data():
    if os.path.exists("safety_incidents.csv"):
        df = pd.read_csv("safety_incidents.csv")
    else:
        df = pd.DataFrame(columns=["Incident ID", "Date", "Time", "Shift", "Location",
                                    "Department", "Incident Type", "Severity",
                                    "Injury Status", "Lost-Time Injury Status", "Cause",
                                    "Corrective Action", "Incident Status"])
    return df

def severity_from_injury(injury_status):
    if injury_status == "No Injury" or injury_status == "First Aid Only":
        return "Minor"
    elif injury_status == "Restricted Work" or injury_status == "Days Away From Work":
        return "Moderate"
    elif injury_status == "Temporary Disability":
        return "Major"
    elif injury_status == "Permanent Disability" or injury_status == "Fatality":
        return "Critical"

def is_lost_time(injury_status):
    if injury_status == "Days Away From Work" or injury_status == "Temporary Disability" or injury_status == "Permanent Disability" or injury_status == "Fatality":
        return "Yes"
    else:
        return "No"

def get_consequence(severity):
    if severity == "Minor":
        return 1
    elif severity == "Moderate":
        return 2
    elif severity == "Major":
        return 4
    elif severity == "Critical":
        return 5


def get_likelihood(department, full_dataframe):
    count = len(full_dataframe[full_dataframe["Department"] == department])

    if count >= 5:
        return 5
    elif count >= 3:
        return 4
    elif count == 2:
        return 3
    elif count == 1:
        return 2
    else:
        return 1


def classify_risk(severity, department, full_dataframe):
    consequence = get_consequence(severity)
    likelihood = get_likelihood(department, full_dataframe)
    score = likelihood * consequence

    if score >= 17:
        classification = "Critical"
    elif score >= 10:
        classification = "High"
    elif score >= 5:
        classification = "Medium"
    else:
        classification = "Low"

    return score, classification

def render_incident_page():
    st.header("Safety Incident Database")

    df = load_data()

    st.subheader("Search & Filter Incidents")
    col1, col2, col3 = st.columns(3)
    with col1:
        dept_filter = st.multiselect("Department", sorted(df["Department"].unique()))
    with col2:
        shift_filter = st.multiselect("Shift", sorted(df["Shift"].unique()))
    with col3:
        severity_filter = st.multiselect("Severity", sorted(df["Severity"].unique()))

    search_term = st.text_input("Search (ID, location, type or cause)")

    filtered = df.copy()
    if dept_filter:
        filtered = filtered[filtered["Department"].isin(dept_filter)]
    if shift_filter:
        filtered = filtered[filtered["Shift"].isin(shift_filter)]
    if severity_filter:
        filtered = filtered[filtered["Severity"].isin(severity_filter)]
    if search_term:
        mask = (filtered["Incident ID"].str.contains(search_term, case=False)
                | filtered["Location"].str.contains(search_term, case=False)
                | filtered["Incident Type"].str.contains(search_term, case=False)
                | filtered["Cause"].str.contains(search_term, case=False))
        filtered = filtered[mask]

    st.dataframe(filtered)
    st.caption(f"Showing {len(filtered)} of {len(df)} incidents")

    st.subheader("Report New Incident")

    with st.form("add_incident_form", clear_on_submit=True):
        incident_date = st.date_input("Date")
        incident_time = st.time_input("Time")
        location = st.text_input("Location")
        department = st.selectbox("Department", ["Mining Operations", "Maintenance",
                                                    "Processing Plant", "Haulage", "Drilling", "Safety"])
        incident_type = st.selectbox("Incident Type", ["Slip/Trip/Fall", "Struck by Object",
                                                        "Struck by Rock/Rockfall", "Vehicle Motion Incident",
                                                        "Pit/Ground Collapse", "Trapped Between Equipment",
                                                        "Fall from Height", "Hit by Moving Equipment",
                                                        "Falling Object", "Equipment Malfunction",
                                                        "Fire", "Electrical Fault", "Chemical Exposure"])
        injury_status = st.selectbox("Injury Status", ["No Injury", "First Aid Only", "Restricted Work",
                                                        "Days Away From Work", "Temporary Disability",
                                                        "Permanent Disability", "Fatality"])
        cause = st.selectbox("Cause", ["Human Error", "Equipment Failure", "Procedure Not Followed",
                                        "Environmental Conditions", "Inadequate Training", "Unknown"])
        corrective_action = st.text_area("Corrective Action", "Investigation ongoing")
        incident_status = st.selectbox("Incident Status", ["Open", "Under Investigation", "Closed"])
        submitted = st.form_submit_button("Log Incident")

    if submitted:
        shift = "Day" if 6 <= incident_time.hour < 18 else "Night"
        incident_id = f"INC-{len(df) + 1:03d}"
        severity = severity_from_injury(injury_status)
        lost_time = is_lost_time(injury_status)

        new_row = {
            "Incident ID": incident_id, "Date": str(incident_date), "Time": incident_time.strftime("%H:%M"),
            "Shift": shift, "Location": location, "Department": department,
            "Incident Type": incident_type, "Severity": severity, "Injury Status": injury_status,
            "Lost-Time Injury Status": lost_time, "Cause": cause,
            "Corrective Action": corrective_action, "Incident Status": incident_status,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("safety_incidents.csv", index=False)
        st.success(f"Incident {incident_id} logged. Severity: {severity}, Lost-Time: {lost_time}")

    st.subheader("Incident Counts & Trends")

    major_critical = len(df[df["Severity"].isin(["Major", "Critical"])])
    lost_time_count = len(df[df["Lost-Time Injury Status"] == "Yes"])

    m1, m2, m3 = st.columns(3)
    m1.metric("Total incidents", len(df))
    m2.metric("Major / Critical", major_critical)
    m3.metric("Lost-time injuries", lost_time_count)

    chart1, chart2 = st.columns(2)
    with chart1:
        st.write("Incidents by department")
        st.bar_chart(df["Department"].value_counts())
    with chart2:
        st.write("Incidents by type")
        st.bar_chart(df["Incident Type"].value_counts())

    st.write("Day vs Night shift")
    st.bar_chart(df["Shift"].value_counts())

    st.write("Incidents per month (trend)")
    months = pd.to_datetime(df["Date"]).dt.to_period("M").astype(str)
    st.line_chart(months.value_counts().sort_index())

    st.subheader("Risk Assessment")

    risk_scores = []
    risk_classes = []
    for index, row in df.iterrows():
        score, classification = classify_risk(row["Severity"], row["Department"], df)
        risk_scores.append(score)
        risk_classes.append(classification)

    df["Risk Score"] = risk_scores
    df["Risk Classification"] = risk_classes

    st.dataframe(df)

    high_critical = df[(df["Risk Classification"] == "High") | (df["Risk Classification"] == "Critical")]
    st.subheader("High & Critical Risks — Require Immediate Attention")
    st.dataframe(high_critical)