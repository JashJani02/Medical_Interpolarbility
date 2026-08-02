import pandas as pd
import plotly.express as px
import streamlit as st

from services.session import SessionManager
from services.supabase_service import SupabaseService

st.set_page_config(
    page_title="Team Workspace",
    page_icon="📋",
    layout="wide"
)

# ==========================================================
# Supabase
# ==========================================================

supabase = SupabaseService.get_client()

# ==========================================================
# Current User (from Google OAuth session)
# ==========================================================

SessionManager.initialize()

# App session is the source of truth
if not SessionManager.is_logged_in():

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.admin = None

    st.warning("Your login session has expired. Please sign in again.")

    st.switch_page("pages/1_login.py")
    st.stop()

# Session is valid
user = SessionManager.get_user()

# Keep Streamlit session synchronized
st.session_state.logged_in = True
st.session_state.user = user

# Tasks are assigned to admin UUIDs (Supabase auth ids). With direct Google
# OAuth we no longer have a Supabase auth id, so resolve the current user's
# admin row by email; fall back to the Google oauth_id/email.
current_user_id = user.get("oauth_id") or user.get("email")

try:
    admin_row = (
        supabase
        .table("admins")
        .select("id")
        .eq("email", user.get("email"))
        .limit(1)
        .execute()
    )
    if admin_row.data:
        current_user_id = admin_row.data[0]["id"]
except Exception:
    pass

display_name = (
    user.get("name")
    or user.get("full_name")
    or user.get("email")
)

#st.write("Current Session")
#st.write(supabase.auth.get_session())

#st.write("Current User")
#st.write(supabase.auth.get_user())

#st.write("Logged In:", st.session_state.logged_in)

#st.write("Stored User:", st.session_state.user)
# ==========================================================
# Database Helpers
# ==========================================================

#@st.cache_data(ttl=300)
def get_admins():

    supabase = SupabaseService.get_client()

    response = (
        supabase
        .table("admins")
        .select("id, full_name")
        .execute()
    )

    return pd.DataFrame(response.data)


#@st.cache_data(ttl=300)
def get_tasks():

    supabase = SupabaseService.get_client()

    response = (
        supabase
        .table("tasks")
        .select("*")
        .execute()
    )

    #st.write("Current User ID")
    #st.write(st.session_state.user.id)

    #st.write("Tasks Response")
    #st.write(response)

    #st.write("Tasks Data")
    #st.write(response.data)

    #st.write("Stored Session User")
    #st.write(st.session_state.user.id)

    #st.write("Supabase Current User")
    #st.write(supabase.auth.get_user())

    #st.write("Current Session")
    #st.write(supabase.auth.get_session())

    task_df = pd.DataFrame(response.data)

    #st.write("Task DF")
    #st.write(task_df)

    admins = (
        supabase
        .table("admins")
        .select("id,full_name")
        .execute()
    )

    #st.write("Admins")
    #st.write(admins.data)

    admin_df = pd.DataFrame(admins.data)

    if task_df.empty:
        return task_df

    admin_map = (
    admin_df
    .set_index("id")["full_name"]
    .to_dict()
)

    task_df["assigned_name"] = task_df["assigned_to"].map(admin_map)



    #st.write("TTASK DF MERGED CLUMNS")
    #st.write(task_df.columns.tolist())
    #st.write(task_df.head())

    return task_df


def create_task(
    title,
    assigned_to,
    status,
    progress,
    start_date,
    end_date
):

    supabase = SupabaseService.get_client()

    (
        supabase
        .table("tasks")
        .insert({
            "title": title,
            "assigned_to": assigned_to,
            "status": status,
            "progress": progress,
            "start_date": str(start_date),
            "end_date": str(end_date)
        })
        .execute()
    )

    st.cache_data.clear()


def update_task(
    task_id,
    status,
    progress,
    start_date,
    end_date
):

    supabase = SupabaseService.get_client()

    (
        supabase
        .table("tasks")
        .update({
            "status": status,
            "progress": progress,
            "start_date": str(start_date),
            "end_date": str(end_date)
        })
        .eq("id", task_id)
        .execute()
    )

    st.cache_data.clear()


def delete_task(task_id):

    supabase = SupabaseService.get_client()

    (
        supabase
        .table("tasks")
        .delete()
        .eq("id", task_id)
        .execute()
    )

    st.cache_data.clear()


# ==========================================================
# Load Data
# ==========================================================

df = get_tasks()
#st.write("Rows:", len(df))
#st.write(df)

#st.write("====================================")
#st.write("Current User ID:", current_user_id)

#st.write("DataFrame shape:", df.shape)

#st.write("assigned_to dtype:", df["assigned_to"].dtype)

#st.write("current_user_id type:", type(current_user_id))

#st.write(df["assigned_to"])

#st.write(df["assigned_to"] == current_user_id)

#st.write(df[df["assigned_to"] == current_user_id])

admins_df = get_admins()

st.title("📋 Team Workspace")

st.write(f"Welcome **{display_name}**")

#st.write("df.empty =", df.empty)
#st.write("len(df) =", len(df))

if df.empty:

    st.warning("No tasks available.")

    st.stop()

# ==========================================================
# Dashboard KPI
# ==========================================================

overall_progress = round(
    df["progress"].mean(),
    2
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Overall Progress",
        f"{overall_progress}%"
    )

with col2:

    st.metric(
        "Total Tasks",
        len(df)
    )

with col3:

    st.metric(
        "Completed",
        (df["status"] == "Completed").sum()
    )

st.progress(overall_progress / 100)

st.divider()


# ==========================================================
# Create Task
# ==========================================================

st.subheader("➕ Create Task")

with st.form("create_task_form"):

    title = st.text_input("Task Title")

    assigned_admin = st.selectbox(
        "Assign To",
        admins_df["full_name"].tolist()
    )

    assigned_id = admins_df.loc[
        admins_df["full_name"] == assigned_admin,
        "id"
    ].iloc[0]

    status = st.selectbox(
        "Status",
        [
            "In Progress",
            "Completed",
            "Delayed"
        ]
    )

    progress = st.slider(
        "Progress",
        0,
        100,
        0
    )

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "Start Date"
        )

    with col2:

        end_date = st.date_input(
            "End Date"
        )

    submitted = st.form_submit_button(
        "Create Task"
    )

    if submitted:

        if title.strip() == "":

            st.error("Task title cannot be empty.")

        elif end_date < start_date:

            st.error("End date cannot be before start date.")

        else:

            create_task(
                title,
                assigned_id,
                status,
                progress,
                start_date,
                end_date
            )

            st.success("Task Created")

            st.rerun()


st.divider()


# ==========================================================
# My Tasks
# ==========================================================

st.subheader("📌 My Tasks")

my_tasks = df[
    df["assigned_to"] == current_user_id
]

if my_tasks.empty:

    st.info("You have no assigned tasks.")

else:

    for _, task in my_tasks.iterrows():

        with st.expander(task["title"]):

            status = st.selectbox(
                "Status",
                [
                    "Completed",
                    "In Progress",
                    "Delayed"
                ],
                index=[
                    "Completed",
                    "In Progress",
                    "Delayed"
                ].index(task["status"]),
                key=f"status_{task['id']}"
            )

            progress = st.slider(
                "Progress",
                0,
                100,
                int(task["progress"]),
                key=f"progress_{task['id']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                start = st.date_input(
                    "Start",
                    value=pd.to_datetime(task["start_date"]),
                    key=f"start_{task['id']}"
                )

            with col2:

                end = st.date_input(
                    "End",
                    value=pd.to_datetime(task["end_date"]),
                    key=f"end_{task['id']}"
                )

            save_col, delete_col = st.columns(2)

            with save_col:

                if st.button(
                    "💾 Save",
                    key=f"save_{task['id']}"
                ):

                    update_task(
                        task["id"],
                        status,
                        progress,
                        start,
                        end
                    )

                    st.success("Task Updated")

                    st.rerun()

            with delete_col:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{task['id']}"
                ):

                    delete_task(task["id"])

                    st.success("Task Deleted")

                    st.rerun()

# ==========================================================
# Timeline
# ==========================================================

st.divider()

st.subheader("📈 Project Timeline")

timeline_df = df.copy()

fig = px.timeline(

    timeline_df,

    x_start="start_date",

    x_end="end_date",

    y="assigned_name",

    color="status",

    hover_name="title",

    text="progress"

)

fig.update_yaxes(

    autorange="reversed"

)

fig.update_layout(

    height=500

)

st.plotly_chart(

    fig,

    use_container_width=True

)


# ==========================================================
# All Project Tasks
# ==========================================================

st.divider()

st.subheader("📋 All Project Tasks")

table_df = df.copy()

table_df.rename(

    columns={

        "title": "Title",

        "assigned_name": "Assigned To",

        "status": "Status",

        "progress": "Progress (%)",

        "start_date": "Start Date",

        "end_date": "End Date"

    },

    inplace=True

)

st.dataframe(

    table_df[

        [

            "Title",

            "Assigned To",

            "Status",

            "Progress (%)",

            "Start Date",

            "End Date"

        ]

    ],

    use_container_width=True,

    hide_index=True

)