import streamlit as st
import worker_safety
import incidents
import equipment

def render_dashboard_page():
    st.header("Mining Monitoring Dashboard")

    workers = worker_safety.load_data()
    inc = incidents.load_data()
    eq = equipment.load_data()

    critical_alerts = 0
    warning_alerts = 0
    for index, row in eq.iterrows():
        status, messages = equipment.check_equipment_condition(row)
        if status == "CRITICAL":
            critical_alerts += 1
        elif status == "WARNING":
            warning_alerts += 1

    st.subheader("Health & Safety")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total workers", len(workers))
    c2.metric("Total incidents", len(inc))
    c3.metric("Near misses", int(workers["Near Misses"].sum()))
    c4.metric("High-risk workers", len(workers[workers["Risk Level"].isin(["High", "Critical"])]))
    st.metric("Average PPE compliance", f"{workers['PPE Compliance (%)'].mean():.1f}%")

    st.subheader("Equipment")
    under_maintenance = len(eq[eq["Maintenance Status"] == "Under Maintenance"])
    e1, e2, e3, e4, e5 = st.columns(5)
    e1.metric("Total equipment", len(eq))
    e2.metric("Available", len(eq) - under_maintenance)
    e3.metric("Under maintenance", under_maintenance)
    e4.metric("Avg availability", f"{eq['Availability (%)'].mean():.1f}%")
    e5.metric("Critical alerts", critical_alerts)
    st.caption(f"{warning_alerts} more units are at WARNING level. "
               "Thresholds are educational prototype values only.")