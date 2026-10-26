import streamlit as st
import worker_safety
import incidents
import equipment
import dashboard
import alerts
import analysis
import reports
import users

st.set_page_config(page_title="Khwezi Mining", page_icon="⛏️", layout="wide", initial_sidebar_state="expanded")


def apply_app_theme():
    """Apply Khwezi Mining's navy and ice-blue theme to every page."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

        :root {
            --khwezi-bg: #0b1220;
            --khwezi-panel: #111c2e;
            --khwezi-panel-2: #17253a;
            --khwezi-blue: #7dd3fc;
            --khwezi-blue-strong: #38bdf8;
            --khwezi-text: #edf6ff;
            --khwezi-muted: #a8bad0;
            --khwezi-border: rgba(125, 211, 252, .22);
        }

        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            font-family: 'DM Sans', sans-serif !important;
        }
        .stApp {
            color: var(--khwezi-text) !important;
            background:
                radial-gradient(ellipse at 10% 0%, rgba(56,189,248,.14), transparent 36rem),
                linear-gradient(145deg, #0b1220 0%, #101b2d 55%, #0b1220 100%) !important;
        }
        [data-testid="stHeader"] { background: rgba(11,18,32,.85) !important; }
        [data-testid="stToolbar"] { right: 1rem; }
        .block-container { max-width: 1440px; padding-top: 2rem; padding-bottom: 3rem; }

        h1, h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            color: var(--khwezi-blue) !important;
            font-family: 'Manrope', sans-serif !important;
            letter-spacing: -.025em;
        }
        p, label, li, span, div[data-testid="stCaptionContainer"] {
            /* Keep body copy readable while allowing specific component colours below. */
        }
        .stMarkdown, [data-testid="stMarkdownContainer"],
        [data-testid="stText"], [data-testid="stCaptionContainer"] {
            color: var(--khwezi-text);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1220 0%, #14243a 100%) !important;
            border-right: 1px solid var(--khwezi-border);
        }
        [data-testid="stSidebar"] * { color: #eaf6ff; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #c2d6e9; }
        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            padding: .55rem .7rem; border-radius: 10px; transition: background .15s ease;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: rgba(125,211,252,.12); }

        div[data-testid="stMetric"],
        [data-testid="stExpander"],
        [data-testid="stForm"],
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(17,28,46,.82) !important;
            border: 1px solid var(--khwezi-border) !important;
            border-radius: 15px !important;
        }
        div[data-testid="stMetric"] { padding: 1rem 1.2rem; box-shadow: 0 8px 24px rgba(0,0,0,.16); }
        div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] * { color: var(--khwezi-muted) !important; }
        div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] * { color: var(--khwezi-blue) !important; font-family: 'Manrope', sans-serif; font-weight: 800; }

        div[data-testid="stButton"] > button,
        div[data-testid="stFormSubmitButton"] > button,
        [data-testid="stDownloadButton"] > button {
            background: linear-gradient(135deg, #0284c7, #38bdf8) !important;
            color: #061322 !important; border: 1px solid rgba(186,230,253,.35) !important;
            border-radius: 10px !important; font-weight: 800 !important;
            transition: transform .15s ease, box-shadow .15s ease;
        }
        div[data-testid="stButton"] > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover,
        [data-testid="stDownloadButton"] > button:hover {
            box-shadow: 0 6px 20px rgba(56,189,248,.25) !important; transform: translateY(-1px);
        }
        input, textarea,
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stDateInput"] input,
        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
            background-color: #0e192a !important; color: #edf6ff !important;
            border-color: var(--khwezi-border) !important; border-radius: 10px !important;
        }
        [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
            background-color: #142238 !important; color: #edf6ff !important;
        }
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            border: 1px solid var(--khwezi-border) !important; border-radius: 12px; overflow: hidden;
        }
        [data-testid="stAlert"] { border-radius: 12px !important; }
        hr { border-color: var(--khwezi-border) !important; }
        a { color: var(--khwezi-blue) !important; }
        [data-testid="stProgressBar"] > div > div { background-color: var(--khwezi-blue-strong) !important; }

        @media (max-width: 768px) {
            .block-container { padding: 1rem 1rem 2rem; }
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
                background:linear-gradient(135deg,#0b1220,#172b43);
                border:1px solid rgba(125,211,252,.42);
                border-radius:22px 22px 0 0; margin-top:3rem;">
                <div style="font-size:2.4rem;">⛏️</div>
                <div style="color:#fff;font-size:1.8rem;font-weight:800;
                    letter-spacing:-.04em;">KHWEZI MINING</div>
                <div style="color:#bae6fd;font-size:.9rem;margin-top:.35rem;">
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
                    <div style="font-size:.78rem;color:#bae6fd;">
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