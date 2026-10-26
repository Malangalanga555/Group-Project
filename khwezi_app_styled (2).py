import streamlit as st
import worker_safety
import incidents
import equipment
import dashboard
import alerts
import analysis
import reports
import users


def apply_app_theme():
    """Apply a consistent, modern visual style to the Streamlit app."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

        :root {
            --khwezi-navy: #101a2c;
            --khwezi-teal: #20b8a6;
            --khwezi-text: #172033;
            --khwezi-muted: #667085;
            --khwezi-background: #f4f7fb;
            --khwezi-border: #e4eaf2;
        }

        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
        .stApp {
            background:
                radial-gradient(circle at 5% 0%, rgba(32,184,166,.08), transparent 25rem),
                var(--khwezi-background);
            color: var(--khwezi-text);
        }
        .block-container {
            max-width: 1440px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3 {
            font-family: 'Manrope', sans-serif !important;
            letter-spacing: -0.035em;
            color: var(--khwezi-navy);
        }
        h1 { font-weight: 800 !important; }
        h2, h3 { font-weight: 700 !important; }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #101a2c 0%, #172b43 100%);
            border-right: 1px solid rgba(255,255,255,.08);
        }
        [data-testid="stSidebar"] * { color: #eef5ff; }
        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            padding: .55rem .7rem;
            border-radius: 10px;
            transition: background 150ms ease;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
            background: rgba(255,255,255,.09);
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #d5e2f1;
        }

        div[data-testid="stMetric"] {
            background: #fff;
            border: 1px solid var(--khwezi-border);
            padding: 1.15rem 1.25rem;
            border-radius: 16px;
            box-shadow: 0 5px 18px rgba(16,26,44,.045);
        }
        div[data-testid="stMetricLabel"] { color: var(--khwezi-muted); font-weight: 600; }
        div[data-testid="stMetricValue"] {
            color: var(--khwezi-navy);
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
        }

        div[data-testid="stButton"] > button,
        div[data-testid="stFormSubmitButton"] > button {
            border: 0;
            border-radius: 10px;
            padding: .55rem 1rem;
            font-weight: 700;
            color: #fff;
            background: linear-gradient(135deg, #159b91, #20b8a6);
            transition: transform 150ms ease, box-shadow 150ms ease;
        }
        div[data-testid="stButton"] > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            color: #fff;
            box-shadow: 0 6px 16px rgba(32,184,166,.25);
            transform: translateY(-1px);
        }
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            border-radius: 10px;
        }
        div[data-testid="stDataFrame"], div[data-testid="stTable"] {
            border: 1px solid var(--khwezi-border);
            border-radius: 12px;
            overflow: hidden;
        }
        div[data-testid="stAlert"] { border-radius: 12px; }
        hr { border-color: var(--khwezi-border); }

        @media (max-width: 768px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_styled_login_page():
    """A welcoming login page that keeps the existing login validation."""
    left, center, right = st.columns([1, 1.15, 1])
    with center:
        st.markdown(
            """
            <div style="text-align:center; padding:1.6rem 1.2rem 1rem;
                background:linear-gradient(135deg,#101a2c,#1d3c54);
                border:1px solid rgba(32,184,166,.35);
                border-radius:22px 22px 0 0; margin-top:3rem;">
                <div style="font-size:2.4rem;">⛏️</div>
                <div style="color:#fff;font-size:1.8rem;font-weight:800;
                    letter-spacing:-.04em;">KHWEZI MINING</div>
                <div style="color:#9ce9df;font-size:.9rem;margin-top:.35rem;">
                    Equipment • Safety • Operations
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            st.markdown("### Welcome back")
            st.caption("Sign in to access your mining operations workspace.")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Log in", use_container_width=True):
                role = users.check_login(username, password)
                if role is not None:
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = role
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")



def login_page():
    render_styled_login_page()


def main():
    apply_app_theme()
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"] == False:
        login_page()
    else:
        current_role = st.session_state["role"]
        with st.sidebar:
            st.markdown(
                """
                <div style="padding:.6rem 0 1rem;">
                    <div style="font-size:1.6rem;">⛏️</div>
                    <div style="font-size:1.15rem;font-weight:800;letter-spacing:-.03em;">
                        KHWEZI MINING
                    </div>
                    <div style="font-size:.78rem;color:#9ce9df;">
                        Operations workspace
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.divider()
            st.caption(f"Signed in as: {st.session_state.get('username', 'User')}")
            st.write(f"Role: **{current_role}**")

        menu_options = ["Dashboard", "Alerts", "Data Analysis", "Reports"]

        if current_role != "Maintenance Engineer":
            menu_options.append("Worker Safety")
            menu_options.append("Safety Incidents")

        if current_role != "Safety Officer":
            menu_options.append("Equipment")

        if current_role == "Administrator":
            menu_options.append("Manage Users")

        with st.sidebar:
            st.markdown("#### Workspace")
            choice = st.radio("Navigate", menu_options, label_visibility="collapsed")

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

        with st.sidebar:
            st.divider()
            if st.button("Log out", use_container_width=True):
                st.session_state["logged_in"] = False
                st.rerun()


main()