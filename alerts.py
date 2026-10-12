import streamlit as st
import worker_safety
import incidents
import equipment


def make_alert(level, id_label, item_id, parameter, value, status, action):
    return {"level": level, "id_label": id_label, "id": item_id,
            "parameter": parameter, "value": value,
            "status": status, "action": action}


def build_alerts(include_safety, include_equipment):
    alerts = []

    if include_equipment:
        eq = equipment.load_data()
        for index, row in eq.iterrows():
            eid = row["Equipment ID"]
            temp = row["Temperature (C)"]
            vib = row["Vibration (mm/s)"]

            if temp > 100:
                alerts.append(make_alert("CRITICAL", "Equipment ID", eid, "Temperature", f"{temp} C",
                                         "Above Critical Threshold",
                                         "Inspect equipment and initiate appropriate maintenance/safety procedures."))
            elif temp >= 80:
                alerts.append(make_alert("WARNING", "Equipment ID", eid, "Temperature", f"{temp} C",
                                         "Approaching Threshold",
                                         "Monitor closely and schedule an inspection."))

            if vib > 8:
                alerts.append(make_alert("CRITICAL", "Equipment ID", eid, "Vibration", f"{vib} mm/s",
                                         "Above Critical Threshold",
                                         "Inspect equipment and initiate appropriate maintenance/safety procedures."))
            elif vib >= 5:
                alerts.append(make_alert("WARNING", "Equipment ID", eid, "Vibration", f"{vib} mm/s",
                                         "Approaching Threshold",
                                         "Monitor closely and schedule an inspection."))

            if row["Maintenance Status"] == "Overdue":
                alerts.append(make_alert("WARNING", "Equipment ID", eid, "Maintenance", "Overdue",
                                         "Overdue Maintenance",
                                         "Schedule maintenance immediately."))

            if row["Downtime (hrs)"] > 150:
                alerts.append(make_alert("WARNING", "Equipment ID", eid, "Downtime",
                                         f"{row['Downtime (hrs)']} hrs",
                                         "Excessive Downtime",
                                         "Investigate the causes of downtime."))

    if include_safety:
        workers = worker_safety.load_data()
        for index, row in workers.iterrows():
            wid = row["Worker ID"]
            ppe = row["PPE Compliance (%)"]

            if ppe < 60:
                alerts.append(make_alert("CRITICAL", "Worker ID", wid, "PPE Compliance", f"{ppe}%",
                                         "Below Critical Threshold",
                                         "Reissue PPE and verify compliance before work continues."))
            elif ppe < 80:
                alerts.append(make_alert("WARNING", "Worker ID", wid, "PPE Compliance", f"{ppe}%",
                                         "Low PPE Compliance",
                                         "Remind worker of PPE requirements and re-check."))

            if row["Fatigue Level"] == "High":
                alerts.append(make_alert("WARNING", "Worker ID", wid, "Fatigue Level", "High",
                                         "High Fatigue",
                                         "Consider rest or reassignment before continuing the shift."))

            if row["Risk Level"] == "Critical":
                alerts.append(make_alert("CRITICAL", "Worker ID", wid, "Risk Level", "Critical",
                                         "High-Risk Safety Observation",
                                         "Supervisor review required immediately."))
            elif row["Risk Level"] == "High":
                alerts.append(make_alert("WARNING", "Worker ID", wid, "Risk Level", "High",
                                         "High-Risk Safety Observation",
                                         "Supervisor review recommended."))

        inc = incidents.load_data()
        for index, row in inc.iterrows():
            if row["Severity"] == "Critical" and row["Incident Status"] != "Closed":
                alerts.append(make_alert("CRITICAL", "Incident ID", row["Incident ID"], "Severity", "Critical",
                                         f"Critical Safety Incident ({row['Incident Status']})",
                                         "Complete the investigation and implement corrective action."))

    return alerts


def render_alerts_page(role):
    st.header("Alerts & Notifications")
    st.caption("Thresholds are educational prototype values only.")

    include_safety = role != "Maintenance Engineer"
    include_equipment = role != "Safety Officer"

    alerts = build_alerts(include_safety, include_equipment)

    critical = [a for a in alerts if a["level"] == "CRITICAL"]
    warnings = [a for a in alerts if a["level"] == "WARNING"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total alerts", len(alerts))
    c2.metric("Critical", len(critical))
    c3.metric("Warning", len(warnings))

    levels = st.multiselect("Show levels", ["CRITICAL", "WARNING"],
                            default=["CRITICAL", "WARNING"])

    for a in critical + warnings:
        if a["level"] in levels:
            lines = [
                "=" * 53,
                "MINING MONITORING ALERT",
                "=" * 53,
                f"[{a['level']}]",
                f"{a['id_label']}: {a['id']}",
                f"Parameter: {a['parameter']}",
                f"Value: {a['value']}",
                f"Status: {a['status']}",
                "Recommended Action:",
                f"  {a['action']}",
                "=" * 53,
            ]
            st.code("\n".join(lines), language=None)