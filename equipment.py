import os
import pandas as pd
import streamlit as st

def load_data():
    if os.path.exists("equipment.csv"):
        df = pd.read_csv("equipment.csv")
    else:
        df = pd.DataFrame(columns=["Equipment ID", "Equipment Type", "Manufacturer",
                                    "Operating Hours", "Temperature (C)", "Vibration (mm/s)",
                                    "Fuel Consumption (L/h)", "Brake Status", "Tyre Status",
                                    "Engine Status", "Maintenance Status", "Downtime (hrs)",
                                    "Availability (%)"])
    return df

def check_equipment_condition(row):
    status = "NORMAL"
    messages = []

    if row["Temperature (C)"] > 100:
        messages.append("CRITICAL: Equipment temperature exceeds predefined threshold. Inspection required.")
        status = "CRITICAL"
    elif row["Temperature (C)"] >= 80:
        messages.append("WARNING: Equipment temperature approaching predefined threshold.")
        status = "WARNING"

    if row["Vibration (mm/s)"] > 8:
        messages.append("CRITICAL: Equipment vibration exceeds predefined threshold. Inspection required.")
        status = "CRITICAL"
    elif row["Vibration (mm/s)"] >= 5:
        messages.append("WARNING: Equipment vibration approaching predefined threshold.")
        if status != "CRITICAL":
            status = "WARNING"

    if status == "NORMAL":
        messages.append("NORMAL: Equipment operating within defined monitoring limits.")

    return status, messages



def check_maintenance(row):
    flags = []

    if row["Maintenance Status"] == "Overdue":
        flags.append("OVERDUE: Maintenance is overdue. Schedule immediately.")
    elif row["Maintenance Status"] == "Due":
        flags.append("DUE: Maintenance is due soon.")
    elif row["Maintenance Status"] == "Under Maintenance":
        flags.append("INFO: Equipment is currently under maintenance.")

    if row["Downtime (hrs)"] > 150:
        flags.append(f"WARNING: Excessive downtime ({row['Downtime (hrs)']} hrs).")

    if row["Availability (%)"] < 85:
        flags.append(f"WARNING: Low availability ({row['Availability (%)']}%).")

    return flags

def render_equipment_page():
    st.header("Equipment Monitoring")
    st.caption("Note: temperature and vibration thresholds are educational prototype values only "
               "and must not be interpreted as actual manufacturer or mine safety limits.")

    df = load_data()
    st.dataframe(df)

    st.subheader("Equipment Condition Alerts")
    normal_count = 0
    for index, row in df.iterrows():
        status, messages = check_equipment_condition(row)
        label = f"{row['Equipment ID']} ({row['Equipment Type']}): " + " | ".join(messages)
        if status == "CRITICAL":
            st.error(label)
        elif status == "WARNING":
            st.warning(label)
        else:
            normal_count += 1

    st.success(f"{normal_count} of {len(df)} units are operating within defined monitoring limits.")

    st.subheader("Maintenance Monitoring")
    for index, row in df.iterrows():
        flags = check_maintenance(row)
        if flags:
            st.warning(f"{row['Equipment ID']} ({row['Equipment Type']}): " + " | ".join(flags))

    st.subheader("Add New Equipment")

    with st.form("add_equipment_form", clear_on_submit=True):
        equipment_type = st.selectbox("Equipment Type", ["Haul Truck", "Loader", "Excavator",
                                                          "Drilling Machine", "Bulldozer",
                                                          "Scraper Winch", "Crusher", "Conveyor"])
        manufacturer = st.selectbox("Manufacturer", ["Caterpillar", "Komatsu", "Liebherr",
                                                      "Sandvik", "Epiroc", "Hitachi"])
        operating_hours = st.number_input("Operating Hours", min_value=0, value=0)
        temperature = st.number_input("Temperature (C)", value=60.0, step=0.5)
        vibration = st.number_input("Vibration (mm/s)", min_value=0.0, value=3.0, step=0.1)
        fuel = st.number_input("Fuel Consumption (L/h)", min_value=0.0, value=30.0, step=0.5)
        brake = st.selectbox("Brake Status", ["Good", "Needs Inspection", "Faulty"])
        tyre = st.selectbox("Tyre Status", ["Good", "Worn", "Needs Replacement"])
        engine = st.selectbox("Engine Status", ["Normal", "Overheating", "Needs Service"])
        maintenance = st.selectbox("Maintenance Status", ["Up to Date", "Due", "Overdue", "Under Maintenance"])
        downtime = st.number_input("Downtime (hrs)", min_value=0, value=0)
        submitted = st.form_submit_button("Add Equipment")

    if submitted:
        equipment_id = f"EQP-{len(df) + 1:03d}"

        total_time = operating_hours + downtime
        if total_time == 0:
            availability = 100.0
        else:
            availability = round(operating_hours / total_time * 100, 1)

        new_row = {
            "Equipment ID": equipment_id, "Equipment Type": equipment_type,
            "Manufacturer": manufacturer, "Operating Hours": operating_hours,
            "Temperature (C)": temperature, "Vibration (mm/s)": vibration,
            "Fuel Consumption (L/h)": fuel, "Brake Status": brake, "Tyre Status": tyre,
            "Engine Status": engine, "Maintenance Status": maintenance,
            "Downtime (hrs)": downtime, "Availability (%)": availability,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("equipment.csv", index=False)

        status, messages = check_equipment_condition(new_row)
        st.success(f"{equipment_id} added. Condition: {status}. Availability: {availability}%")