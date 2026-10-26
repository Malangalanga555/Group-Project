import os
import streamlit as st

# set_page_config must be the first Streamlit command, so it sits above the other imports
st.set_page_config(page_title="Khwezi Mining", page_icon="⛏️", layout="wide")

import worker_safety
import incidents
import equipment
import dashboard
import alerts
import analysis
import reports
import users


ICONS = {
    "Dashboard": "📊",
    "Alerts": "🚨",
    "Data Analysis": "📈",
    "Reports": "📄",
    "Worker Safety": "👷",
    "Safety Incidents": "⚠️",
    "Equipment": "🚜",
    "Manage Users": "👥",
}

STYLE = """
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: none; }
}
.banner {
    background: linear-gradient(90deg, #B45309, #F59E0B);
    padding: 18px 24px;
    border-radius: 12px;
    margin-bottom: 18px;
    animation: fadeIn 0.6s ease-out;
}
.banner-title { color: #111827; font-size: 1.8rem; font-weight: 800; }
.banner-sub   { color: #1F2937; font-size: 1rem; }
[data-testid="stMetric"] {
    background: #1F2937;
    border: 1px solid #374151;
    border-left: 5px solid #F59E0B;
    padding: 14px;
    border-radius: 10px;
}
section[data-testid="stSidebar"] { border-right: 2px solid #F59E0B; }
div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
    border-radius: 8px;
    font-weight: 600;
}
</style>
"""


def show_banner(subtitle):
    st.markdown(
        '<div class="banner">'
        '<div class="banner-title">⛏️ Khwezi Mining</div>'
        '<div class="banner-sub">' + subtitle + '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def login_page():
    left, middle, right = st.columns([1, 2, 1])
    with middle:
        show_banner("Health, Safety & Equipment Monitoring")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Log In")

    if login_button:
        role = users.check_login(username, password)
        if role is not None:
            st.session_state["logged_in"] = True
            st.session_state["role"] = role
            st.session_state["username"] = username
            st.rerun()
        else:
            with middle:
                st.error("Incorrect username or password.")


def main():
    st.markdown(STYLE, unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] == False:
        login_page()
    else:
        current_role = st.session_state["role"]
        current_user = st.session_state.get("username", "")

        if os.path.exists("MINE LOGO.png"):
            st.sidebar.image("MINE LOGO.png", width=200)
        st.sidebar.write(f"Logged in as: {current_user} ({current_role})")

        menu_options = ["Dashboard", "Alerts", "Data Analysis", "Reports"]

        if current_role != "Maintenance Engineer":
            menu_options.append("Worker Safety")
            menu_options.append("Safety Incidents")

        if current_role != "Safety Officer":
            menu_options.append("Equipment")

        if current_role == "Administrator":
            menu_options.append("Manage Users")

        choice = st.sidebar.radio(
            "Navigate",
            menu_options,
            format_func=lambda name: ICONS.get(name, "") + "  " + name,
        )

        show_banner(choice)

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
        elif choice == "Manage Users":
            users.render_manage_users_page()

        if st.sidebar.button("Log Out"):
            st.session_state["logged_in"] = False
            st.rerun()


main()