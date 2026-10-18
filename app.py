
import streamlit as st
from supabase import create_client, Client

st.set_page_config(
    page_title="Class Monitor",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Class Monitor")
st.caption("Manage attendance, assignments, homework and student marks.")

# No login screen. Read database credentials from Streamlit Secrets.
@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"].strip().rstrip("/")
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

try:
    supabase = get_supabase()
    st.success("Connected to Supabase")
except Exception as e:
    st.error("Could not connect to the database.")
    st.caption(
        "Check SUPABASE_URL and SUPABASE_KEY "
        "in Streamlit app settings."
    )
    st.code(str(e))
    st.stop()

section = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Attendance",
        "Assignments & Homework",
        "Student Marks",
    ],
)

if section == "Dashboard":
    st.subheader("Dashboard")
    st.info("Your class overview will appear here.")

elif section == "Attendance":
    st.subheader("Attendance")
    st.info("Attendance management")

elif section == "Assignments & Homework":
    st.subheader("Assignments & Homework")
    st.info("Assignment and homework management")

elif section == "Student Marks":
    st.subheader("Student Marks")
    st.info("Student marks management")
