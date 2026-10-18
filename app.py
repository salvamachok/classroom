
import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(
    page_title="Class Monitor",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Class Monitor")
st.caption("Manage attendance, assignments and student marks.")

# Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Class Monitor Login")
    password = st.text_input("Enter your password", type="password")

    if st.button("Log in", type="primary"):
        if password == st.secrets["APP_PASSWORD"]:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.stop()

# Connect to Supabase
@st.cache_resource
def connect_database():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
    )

try:
    supabase = connect_database()

    def load_data():
        result = (
            supabase.table("class_monitor_state")
            .select("data")
            .eq("id", 1)
            .single()
            .execute()
        )
        return result.data["data"]

    def save_data(data):
        (
            supabase.table("class_monitor_state")
            .update({
                "data": data,
                "updated_at": "now()"
            })
            .eq("id", 1)
            .execute()
        )

    if "class_data" not in st.session_state:
        st.session_state.class_data = load_data()

    data = st.session_state.class_data

    def persist():
        save_data(st.session_state.class_data)

    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Choose a section",
            [
                "Dashboard",
                "Students",
                "Attendance",
                "Assignments",
                "Marks"
            ]
        )

        if st.button("Refresh data"):
            st.session_state.class_data = load_data()
            st.rerun()

        if st.button("Log out"):
            st.session_state.logged_in = False
            st.session_state.pop("class_data", None)
            st.rerun()

    students = data["students"]

    if page == "Dashboard":
        st.subheader("Class Overview")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Students", len(students))
        c2.metric("Assignments", len(data["work"]))
        c3.metric("Mark records", len(data["marks"]))

        attendance_count = sum(
            len(records)
            for records in data["attendance"].values()
        )
        c4.metric("Attendance records", attendance_count)

        st.info(
            "Use the navigation menu to record attendance, "
            "manage assignments and enter marks."
        )

        if students:
            st.dataframe(
                pd.DataFrame(students),
                use_container_width=True,
                hide_index=True
            )

    elif page == "Students":
        st.subheader("Student Register")

        with st.form("add_student", clear_on_submit=True):
            name = st.text_input("Student full name")
            student_id = st.text_input("Student ID / admission number")
            submitted = st.form_submit_button("Add student")

            if submitted:
                if not name.strip() or not student_id.strip():
                    st.error("Enter both the student's name and ID.")
                elif any(
                    s["student_id"].lower() == student_id.strip().lower()
                    for s in students
                ):
                    st.error("That student ID already exists.")
                else:
                    data["students"].append({
                        "student_id": student_id.strip(),
                        "name": name.strip()
                    })
                    persist()
                    st.success("Student added.")
                    st.rerun()

        if students:
            st.dataframe(
                pd.DataFrame(students),
                use_container_width=True,
                hide_index=True
            )

            remove_id = st.selectbox(
                "Select a student to remove",
                options=[s["student_id"] for s in students],
                format_func=lambda sid: next(
                    s["name"] + " (" + sid + ")"
                    for s in students if s["student_id"] == sid
                )
            )

            if st.button("Remove selected student"):
                data["students"] = [
                    s for s in students if s["student_id"] != remove_id
                ]
                for date in data["attendance"]:
                    data["attendance"][date].pop(remove_id, None)
                data["marks"] = [
                    m for m in data["marks"]
                    if m["student_id"] != remove_id
                ]
                persist()
                st.rerun()
        else:
            st.write("No students added yet.")

    elif page == "Attendance":
        st.subheader("Daily Attendance")

        if not students:
            st.warning("Add students first.")
        else:
            date = st.date_input("Attendance date").isoformat()
            current = data["attendance"].get(date, {})

            with st.form("attendance_form"):
                statuses = {}
                for student in students:
                    statuses[student["student_id"]] = st.selectbox(
                        student["name"],
                        ["Present", "Absent", "Late", "Excused"],
                        index=(
                            ["Present", "Absent", "Late", "Excused"]
                            .index(current[student["student_id"]])
                            if student["student_id"] in current
                            else 0
                        ),
                        key="attendance_" + date + "_" + student["student_id"]
                    )

                submitted = st.form_submit_button("Save attendance")

                if submitted:
                    data["attendance"][date] = statuses
                    persist()
                    st.success("Attendance saved.")
                    st.rerun()

            if date in data["attendance"]:
                st.write("Saved attendance")
                st.dataframe(
                    pd.DataFrame([
                        {
                            "Student": s["name"],
                            "ID": s["student_id"],
                            "Status": data["attendance"][date].get(
                                s["student_id"], "Not recorded"
                            )
                        }
                        for s in students
                    ]),
                    use_container_width=True,
                    hide_index=True
                )

    elif page == "Assignments":
        st.subheader("Assignments and Homework")

        with st.form("assignment_form", clear_on_submit=True):
            title = st.text_input("Assignment title")
            subject = st.text_input("Subject")
            due_date = st.date_input("Due date")
            details = st.text_area("Instructions / details")
            submitted = st.form_submit_button("Add assignment")

            if submitted:
                if not title.strip() or not subject.strip():
                    st.error("Enter an assignment title and subject.")
                else:
                    data["work"].append({
                        "title": title.strip(),
                        "subject": subject.strip(),
                        "due_date": due_date.isoformat(),
                        "details": details.strip()
                    })
                    persist()
                    st.success("Assignment added.")
                    st.rerun()

        if data["work"]:
            st.dataframe(
                pd.DataFrame(data["work"]),
                use_container_width=True,
                hide_index=True
            )

            assignment_index = st.selectbox(
                "Choose assignment to delete",
                range(len(data["work"])),
                format_func=lambda i: (
                    data["work"][i]["subject"] + " — "
                    + data["work"][i]["title"]
                )
            )
            if st.button("Delete assignment"):
                data["work"].pop(assignment_index)
                persist()
                st.rerun()

    elif page == "Marks":
        st.subheader("Student Marks")

        if not students:
            st.warning("Add students first.")
        else:
            with st.form("marks_form", clear_on_submit=True):
                student_id = st.selectbox(
                    "Student",
                    [s["student_id"] for s in students],
                    format_func=lambda sid: next(
                        s["name"] for s in students
                        if s["student_id"] == sid
                    )
                )
                subject = st.text_input("Subject")
                assessment = st.text_input("Test / exam / assignment")
                score = st.number_input("Marks obtained", min_value=0.0)
                maximum = st.number_input("Total possible marks", min_value=1.0)
                submitted = st.form_submit_button("Save marks")

                if submitted:
                    if not subject.strip() or not assessment.strip():
                        st.error("Enter the subject and assessment name.")
                    elif score > maximum:
                        st.error("Marks obtained cannot exceed the total.")
                    else:
                        data["marks"].append({
                            "student_id": student_id,
                            "subject": subject.strip(),
                            "assessment": assessment.strip(),
                            "score": score,
                            "maximum": maximum,
                            "percentage": round(score / maximum * 100, 2)
                        })
                        persist()
                        st.success("Marks saved.")
                        st.rerun()

            if data["marks"]:
                names = {
                    s["student_id"]: s["name"] for s in students
                }
                records = [
                    {
                        **m,
                        "student_name": names.get(
                            m["student_id"], "Unknown student"
                        )
                    }
                    for m in data["marks"]
                ]
                st.dataframe(
                    pd.DataFrame(records),
                    use_container_width=True,
                    hide_index=True
                )

                if st.button("Export marks as CSV"):
                    csv = pd.DataFrame(records).to_csv(index=False)
                    st.download_button(
                        "Download marks CSV",
                        data=csv,
                        file_name="class_marks.csv",
                        mime="text/csv"
                    )

except Exception as error:
    st.error("Could not connect to the database or load the data.")
    st.caption("Check your Supabase secrets and SQL setup.")
    st.exception(error)
