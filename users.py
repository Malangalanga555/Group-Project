import os
import pandas as pd
import streamlit as st

USERS_FILE = "users.csv"

ROLES = ["Administrator", "Safety Officer", "Mining Engineer",
         "Maintenance Engineer", "Manager"]

DEFAULT_USERS = [
    {"username": "paballo", "password": "admin123", "role": "Administrator"},
    {"username": "langelihle", "password": "safety123", "role": "Safety Officer"},
    {"username": "bohlale", "password": "maint123", "role": "Maintenance Engineer"},
    {"username": "mkhwanazi", "password": "manager123", "role": "Manager"},
    {"username": "engineer1", "password": "mining123", "role": "Mining Engineer"},
]


def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE, dtype=str)
    user_df = pd.DataFrame(DEFAULT_USERS)
    user_df.to_csv(USERS_FILE, index=False)
    return user_df


def check_login(username, password):
    user_df = load_users()
    match = user_df[(user_df["username"] == username) & (user_df["password"] == password)]
    if len(match) == 1:
        return match.iloc[0]["role"]
    return None


def render_manage_users_page():
    st.header("Manage Users")

    if st.session_state.get("role") != "Administrator":
        st.error("Only the Administrator can manage users.")
        return

    user_df = load_users()

    st.subheader("Current users")
    st.dataframe(user_df[["username", "role"]])

    st.subheader("Add a new user")
    with st.form("add_user_form", clear_on_submit=True):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ROLES)
        submitted = st.form_submit_button("Add User")

    if submitted:
        new_username = new_username.strip()
        if new_username == "" or new_password == "":
            st.error("Username and password are required.")
        elif new_username in list(user_df["username"]):
            st.error("That username already exists.")
        elif len(new_password) < 4:
            st.error("Password must be at least 4 characters.")
        else:
            new_row = {"username": new_username, "password": new_password, "role": new_role}
            user_df = pd.concat([user_df, pd.DataFrame([new_row])], ignore_index=True)
            user_df.to_csv(USERS_FILE, index=False)
            st.success(f"User {new_username} added as {new_role}.")

            st.subheader("Remove a user")
    user_df = load_users()
    username_to_remove = st.selectbox("Select user to remove", list(user_df["username"]))
    confirm = st.checkbox(f"I confirm I want to remove {username_to_remove}")

    if st.button("Remove User"):
        admin_count = len(user_df[user_df["role"] == "Administrator"])
        target_role = user_df[user_df["username"] == username_to_remove].iloc[0]["role"]

        if not confirm:
            st.error("Please tick the confirmation box first.")
        elif target_role == "Administrator" and admin_count <= 1:
            st.error("Cannot remove the last Administrator.")
        else:
            user_df = user_df[user_df["username"] != username_to_remove]
            user_df.to_csv(USERS_FILE, index=False)
            st.success(f"User {username_to_remove} removed.")