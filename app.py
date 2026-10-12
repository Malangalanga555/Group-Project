import streamlit as st
import worker_safety
import incidents
import equipment
import dashboard
import alerts
import analysis
import reports

USERS = {
    "paballo": {"password": "admin123", "role": "Administrator"},
    "langelihle": {"password": "safety123", "role": "Safety Officer"},
    "bohlale": {"password": "maint123", "role": "Maintenance Engineer"},
    "mkhwanazi": {"password": "manager123", "role": "Manager"},
    "engineer1": {"password": "mining123", "role": "Mining Engineer"},
}

def login_page():
    st.header("Khwezi Mining - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Log In")

    if login_button:
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["role"] = USERS[username]["role"]
            st.rerun()
        else:
            st.error("Incorrect username or password.")

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] == False:
        login_page()
    else:
        current_role = st.session_state["role"]
        st.sidebar.write(f"Logged in as: {current_role}")

        menu_options = ["Dashboard", "Alerts", "Data Analysis", "Reports"]

        if current_role != "Maintenance Engineer":
            menu_options.append("Worker Safety")
            menu_options.append("Safety Incidents")

        if current_role != "Safety Officer":
            menu_options.append("Equipment")

        choice = st.sidebar.radio("Navigate", menu_options)

        if choice == "Dashboard":
            dashboard.render_dashboard_page()
        elif choice == "Worker Safety":
            worker_safety.render_worker_safety_page()
        elif choice == "Safety Incidents":
            incidents.render_incident_page()
        elif choice == "Equipment":
            equipment.render_equipment_page()
        elif choice == "Alerts":
            alerts.render_alerts_page(current_role)
        elif choice == "Data Analysis":
            analysis.render_analysis_page(current_role)
        elif choice == "Reports":
            reports.render_reports_page(current_role)

        if st.sidebar.button("Log Out"):
            st.session_state["logged_in"] = False
            st.rerun()

main()