import streamlit as st
import pandas as pd
from datetime import date
import worker_safety
import incidents
import equipment
import alerts


def build_summary(role):
    include_safety = role != "Maintenance Engineer"
    include_equipment = role != "Safety Officer"

    lines = []
    lines.append("KHWEZI MINING - MONITORING SUMMARY REPORT")
    lines.append(f"Date: {date.today()}")
    lines.append(f"Generated for role: {role}")
    lines.append("=" * 50)

    if include_safety:
        workers = worker_safety.load_data()
        inc = incidents.load_data()
        high_risk = len(workers[workers["Risk Level"].isin(["High", "Critical"])])
        lines.append("")
        lines.append("HEALTH AND SAFETY")
        lines.append(f"Total workers: {len(workers)}")
        lines.append(f"Total incidents: {len(inc)}")
        lines.append(f"Near misses recorded: {int(workers['Near Misses'].sum())}")
        lines.append(f"High-risk workers: {high_risk}")
        lines.append(f"Average PPE compliance: {workers['PPE Compliance (%)'].mean():.1f}%")

    if include_equipment:
        eq = equipment.load_data()
        critical_units = 0
        for index, row in eq.iterrows():
            status, messages = equipment.check_equipment_condition(row)
            if status == "CRITICAL":
                critical_units += 1
        under_maintenance = len(eq[eq["Maintenance Status"] == "Under Maintenance"])
        overdue = len(eq[eq["Maintenance Status"] == "Overdue"])
        lines.append("")
        lines.append("EQUIPMENT")
        lines.append(f"Total equipment: {len(eq)}")
        lines.append(f"Under maintenance: {under_maintenance}")
        lines.append(f"Overdue for maintenance: {overdue}")
        lines.append(f"Average availability: {eq['Availability (%)'].mean():.1f}%")
        lines.append(f"Units at CRITICAL condition: {critical_units}")

    all_alerts = alerts.build_alerts(include_safety, include_equipment)
    critical = len([a for a in all_alerts if a["level"] == "CRITICAL"])
    warnings = len([a for a in all_alerts if a["level"] == "WARNING"])
    lines.append("")
    lines.append("ALERTS")
    lines.append(f"Critical alerts: {critical}")
    lines.append(f"Warning alerts: {warnings}")
    lines.append("")
    lines.append("Note: thresholds are educational prototype values only.")

    return "\n".join(lines)


def render_reports_page(role):
    st.header("Generate Reports")
    st.caption("Download a summary report or export the data your role has access to.")

    include_safety = role != "Maintenance Engineer"
    include_equipment = role != "Safety Officer"

    summary = build_summary(role)
    st.subheader("Summary report")
    st.code(summary, language=None)
    st.download_button("Download summary report (.txt)", summary,
                       file_name="khwezi_summary_report.txt")

    st.subheader("Data exports (CSV)")

    if include_safety:
        workers = worker_safety.load_data()
        inc = incidents.load_data()
        st.download_button("Download worker safety data", workers.to_csv(index=False),
                           file_name="worker_safety_export.csv", mime="text/csv")
        st.download_button("Download incident data", inc.to_csv(index=False),
                           file_name="safety_incidents_export.csv", mime="text/csv")

    if include_equipment:
        eq = equipment.load_data()
        st.download_button("Download equipment data", eq.to_csv(index=False),
                           file_name="equipment_export.csv", mime="text/csv")

    all_alerts = alerts.build_alerts(include_safety, include_equipment)
    st.download_button("Download current alerts", pd.DataFrame(all_alerts).to_csv(index=False),
                       file_name="alerts_export.csv", mime="text/csv")