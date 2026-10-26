import streamlit as st
import worker_safety
import incidents
import equipment
import alerts


def show_ranking(df, column, lowest=False):
    if lowest:
        ranked = df.nsmallest(5, column)
    else:
        ranked = df.nlargest(5, column)
    first = ranked.iloc[0]
    st.success(f"{first['Equipment ID']} ({first['Equipment Type']}): {first[column]}")
    st.dataframe(ranked[["Equipment ID", "Equipment Type", column]])


def render_analysis_page(role):
    st.header("Interactive Data Analysis")
    st.caption("Pick a question and the app answers it from the current data.")

    workers = worker_safety.load_data()
    inc = incidents.load_data()
    eq = equipment.load_data()

    safety_questions = [
        "How many safety incidents have occurred?",
        "Which department has the highest number of incidents?",
        "Which shift records the most incidents?",
        "Which incident types occur most frequently?",
        "What are the most common causes of incidents?",
        "How many incidents are classified as High or Critical risk?",
        "How many near misses have been recorded?",
        "What percentage of workers comply with PPE requirements?",
    ]
    equipment_questions = [
        "Which equipment has the highest downtime?",
        "Which equipment has the lowest availability?",
        "Which equipment has the highest vibration?",
        "Which equipment has the highest temperature?",
        "Which equipment requires maintenance?",
        "What is the average equipment availability?",
        "Which equipment type has the highest downtime?",
        "What percentage of equipment is operating normally?",
    ]

    questions = []
    if role != "Maintenance Engineer":
        questions += safety_questions
    if role != "Safety Officer":
        questions += equipment_questions
    if role not in ("Maintenance Engineer", "Safety Officer"):
        questions.append("How many critical alerts are currently active?")

    question = st.selectbox("Choose a question", questions)
    st.subheader("Answer")

    if question == "How many safety incidents have occurred?":
        st.metric("Total incidents", len(inc))

    elif question == "Which department has the highest number of incidents?":
        counts = inc["Department"].value_counts()
        st.success(f"{counts.index[0]} has the most incidents ({counts.iloc[0]}).")
        st.bar_chart(counts)

    elif question == "Which shift records the most incidents?":
        counts = inc["Shift"].value_counts()
        st.success(f"The {counts.index[0]} shift has the most incidents ({counts.iloc[0]}).")
        st.bar_chart(counts)

    elif question == "Which incident types occur most frequently?":
        counts = inc["Incident Type"].value_counts()
        st.success(f"{counts.index[0]} is the most frequent type ({counts.iloc[0]}).")
        st.bar_chart(counts)

    elif question == "What are the most common causes of incidents?":
        counts = inc["Cause"].value_counts()
        st.success(f"{counts.index[0]} is the most common cause ({counts.iloc[0]}).")
        st.bar_chart(counts)

    elif question == "How many incidents are classified as High or Critical risk?":
        count = 0
        for index, row in inc.iterrows():
            score, classification = incidents.classify_risk(row["Severity"], row["Department"], inc)
            if classification in ("High", "Critical"):
                count += 1
        st.metric("High / Critical risk incidents", count)

    elif question == "How many near misses have been recorded?":
        st.metric("Near misses recorded", int(workers["Near Misses"].sum()))

    elif question == "What percentage of workers comply with PPE requirements?":
        compliant = workers["PPE Compliance (%)"] >= 80
        st.metric("Workers at 80% PPE compliance or above", f"{compliant.mean() * 100:.1f}%")
        st.caption("Assumption: a worker counts as compliant at 80% or above.")

    elif question == "Which equipment has the highest downtime?":
        show_ranking(eq, "Downtime (hrs)")

    elif question == "Which equipment has the lowest availability?":
        show_ranking(eq, "Availability (%)", lowest=True)

    elif question == "Which equipment has the highest vibration?":
        show_ranking(eq, "Vibration (mm/s)")

    elif question == "Which equipment has the highest temperature?":
        show_ranking(eq, "Temperature (C)")

    elif question == "Which equipment requires maintenance?":
        needs = eq[eq["Maintenance Status"].isin(["Due", "Overdue"])]
        st.metric("Units due or overdue", len(needs))
        st.dataframe(needs[["Equipment ID", "Equipment Type", "Maintenance Status"]])

    elif question == "What is the average equipment availability?":
        st.metric("Average availability", f"{eq['Availability (%)'].mean():.1f}%")

    elif question == "Which equipment type has the highest downtime?":
        totals = eq.groupby("Equipment Type")["Downtime (hrs)"].sum().sort_values(ascending=False)
        st.success(f"{totals.index[0]} has the highest total downtime ({totals.iloc[0]} hrs).")
        st.bar_chart(totals)

    elif question == "What percentage of equipment is operating normally?":
        normal = 0
        for index, row in eq.iterrows():
            status, messages = equipment.check_equipment_condition(row)
            if status == "NORMAL":
                normal += 1
        st.metric("Operating normally", f"{normal / len(eq) * 100:.1f}%")
        st.caption("Thresholds are educational prototype values only.")

    elif question == "How many critical alerts are currently active?":
        all_alerts = alerts.build_alerts(True, True)
        critical = [a for a in all_alerts if a["level"] == "CRITICAL"]
        st.metric("Critical alerts", len(critical))
