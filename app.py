
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Class Monitor",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Session data
# -----------------------------
DEFAULTS = {
    "students": [],
    "attendance": [],
    "assignments": [],
    "marks": [],
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy()

# -----------------------------
# Pink and black styling
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --pink: #FF4F9A;
    --pink-light: #FFF0F6;
    --pink-border: #FFD0E3;
    --black: #151218;
    --muted: #77717D;
    --white: #FFFFFF;
    --page: #FAF7F9;
    --line: #EDE5EA;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--black);
}

.stApp { background: var(--page); }

h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--black) !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: var(--white);
    border-right: 1px solid var(--line);
}

.brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 8px 22px;
    margin-bottom: 18px;
    border-bottom: 1px solid var(--line);
}

.brand-mark {
    width: 44px;
    height: 44px;
    border-radius: 13px;
    background: var(--pink);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
}

.brand-title {
    font-family: 'Manrope', sans-serif;
    font-size: 16px;
    font-weight: 800;
}

.brand-subtitle {
    color: var(--muted);
    font-size: 11px;
    margin-top: 3px;
}

/* Visible sidebar navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] {
    width: 100%;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    box-sizing: border-box !important;
    padding: 12px !important;
    margin: 0 !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    color: var(--black) !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label p,
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label span {
    color: var(--black) !important;
    opacity: 1 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover,
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    background: var(--pink-light) !important;
    border-color: var(--pink-border) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] input {
    accent-color: var(--pink) !important;
}

.eyebrow {
    color: var(--pink);
    font-size: 11px;
    text-transform: uppercase;
    font-weight: 800;
    letter-spacing: .14em;
    margin-bottom: 7px;
}

.page-title {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(28px, 3vw, 37px);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -.04em;
    margin-bottom: 7px;
}

.page-description {
    color: var(--muted);
    font-size: 14px;
    margin-bottom: 25px;
}

.metric-card {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 20px;
    min-height: 120px;
    box-shadow: 0 3px 12px rgba(21, 18, 24, .025);
}

.metric-label {
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 12px;
}

.metric-value {
    font-family: 'Manrope', sans-serif;
    font-size: 30px;
    font-weight: 800;
}

.metric-note {
    color: var(--muted);
    font-size: 12px;
    margin-top: 9px;
}

.section-heading {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: 18px;
    margin: 25px 0 12px;
}

.empty-state {
    padding: 24px;
    border: 1px dashed var(--pink-border);
    border-radius: 14px;
    color: var(--muted);
    background: var(--white);
    text-align: center;
}

div.stButton > button,
div.stDownloadButton > button,
div[data-testid="stFormSubmitButton"] > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
    border-color: var(--pink);
}

div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: var(--pink) !important;
    border-color: var(--pink) !important;
    color: white !important;
}

div.stDownloadButton > button {
    background: var(--black);
    color: white;
    border-color: var(--black);
}

hr { border-color: var(--line); }

@media (max-width: 768px) {
    .block-container { padding-top: 1.2rem; }
    .metric-card { padding: 15px; }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Helper functions
# -----------------------------
def page_header(title, description):
    st.markdown(
        '<div class="eyebrow">CLASS MONITOR</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="page-title">{title}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="page-description">{description}</div>',
        unsafe_allow_html=True,
    )


def metric_card(label, value, note):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def show_empty(message):
    st.markdown(
        f'<div class="empty-state">{message}</div>',
        unsafe_allow_html=True,
    )


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand-wrap">
        <div class="brand-mark">C</div>
        <div>
            <div class="brand-title">Class Monitor</div>
            <div class="brand-subtitle">Classroom management</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:11px;font-weight:800;'
        'letter-spacing:.12em;color:#77717D;margin:8px 0 10px 8px;">'
        'WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Students",
            "Attendance",
            "Assignments & Homework",
            "Student Marks",
            "Export Data",
        ],
        label_visibility="collapsed",
        key="navigation_page",
    )

    st.markdown("---")
    st.caption(
        "Data is stored in the active session and may reset "
        "when the app restarts."
    )


# -----------------------------
# Dashboard
# -----------------------------
if page == "Dashboard":
    page_header(
        "Class overview",
        "A clear view of your students, attendance, assignments, and marks.",
    )

    total_students = len(st.session_state.students)

    today_records = [
        row for row in st.session_state.attendance
        if row["Date"] == str(date.today())
    ]

    present_today = sum(
        row["Status"] == "Present" for row in today_records
    )

    late_today = sum(
        row["Status"] == "Late" for row in today_records
    )

    attendance_rate = (
        round(present_today / len(today_records) * 100)
        if today_records else 0
    )

    columns = st.columns(5)

    metrics = [
        ("TOTAL STUDENTS", total_students, "Students on your class list"),
        ("PRESENT TODAY", present_today, "Present records for today"),
        ("LATE TODAY", late_today, "Late records for today"),
        ("ATTENDANCE RATE", f"{attendance_rate}%", "Based on today's records"),
        ("ASSIGNMENTS", len(st.session_state.assignments), "Homework and classwork"),
    ]

    for column, metric in zip(columns, metrics):
        with column:
            metric_card(*metric)

    st.markdown(
        '<div class="section-heading">Recent attendance</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.attendance:
        df = pd.DataFrame(st.session_state.attendance)
        st.dataframe(
            df.tail(8).iloc[::-1],
            use_container_width=True,
            hide_index=True,
        )
    else:
        show_empty("No attendance recorded yet. Open Attendance to get started.")

    st.markdown(
        '<div class="section-heading">Recent assignments</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.assignments:
        df = pd.DataFrame(st.session_state.assignments)
        st.dataframe(
            df.tail(5).iloc[::-1],
            use_container_width=True,
            hide_index=True,
        )
    else:
        show_empty("No assignments have been added yet.")


# -----------------------------
# Students
# -----------------------------
elif page == "Students":
    page_header("Students", "Manage your class list.")

    with st.form("add_student_form", clear_on_submit=True):
        name = st.text_input(
            "Student full name",
            placeholder="Enter a student's name",
        )
        submitted = st.form_submit_button(
            "Add student",
            type="primary",
        )

    if submitted:
        name = name.strip()

        if not name:
            st.error("Enter a student name first.")
        elif any(
            existing.casefold() == name.casefold()
            for existing in st.session_state.students
        ):
            st.warning("That student is already on the list.")
        else:
            st.session_state.students.append(name)
            st.success(f"{name} was added.")
            st.rerun()

    st.markdown(
        '<div class="section-heading">Class list</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.students:
        st.dataframe(
            pd.DataFrame(
                st.session_state.students,
                columns=["Student"],
            ),
            use_container_width=True,
            hide_index=True,
        )

        selected = st.selectbox(
            "Select a student to remove",
            st.session_state.students,
        )

        if st.button("Remove selected student"):
            st.session_state.students.remove(selected)

            st.session_state.attendance = [
                row for row in st.session_state.attendance
                if row["Student"] != selected
            ]

            st.session_state.marks = [
                row for row in st.session_state.marks
                if row["Student"] != selected
            ]

            st.success(f"{selected} was removed.")
            st.rerun()
    else:
        show_empty("Your class list is empty. Add your first student above.")


# -----------------------------
# Attendance
# -----------------------------
elif page == "Attendance":
    page_header(
        "Attendance",
        "Record whether each student is present, absent, late, or excused.",
    )

    if not st.session_state.students:
        st.info("Add students first, then return here to record attendance.")
    else:
        with st.form("attendance_form", clear_on_submit=True):
            attendance_date = st.date_input(
                "Attendance date",
                value=date.today(),
            )
            student = st.selectbox(
                "Student",
                st.session_state.students,
            )
            status = st.selectbox(
                "Status",
                ["Present", "Absent", "Late", "Excused"],
            )
            notes = st.text_input("Notes (optional)")

            submitted = st.form_submit_button(
                "Save attendance",
                type="primary",
            )

        if submitted:
            record = {
                "Date": str(attendance_date),
                "Student": student,
                "Status": status,
                "Notes": notes.strip(),
            }

            existing = next(
                (
                    i for i, row in enumerate(st.session_state.attendance)
                    if row["Date"] == record["Date"]
                    and row["Student"] == record["Student"]
                ),
                None,
            )

            if existing is None:
                st.session_state.attendance.append(record)
            else:
                st.session_state.attendance[existing] = record

            st.success("Attendance saved.")
            st.rerun()

    st.markdown(
        '<div class="section-heading">Attendance records</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.attendance:
        df = pd.DataFrame(st.session_state.attendance)
        st.dataframe(
            df.sort_values("Date", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

        index = st.selectbox(
            "Select a record to remove",
            range(len(st.session_state.attendance)),
            format_func=lambda i: (
                f'{st.session_state.attendance[i]["Date"]} — '
                f'{st.session_state.attendance[i]["Student"]} — '
                f'{st.session_state.attendance[i]["Status"]}'
            ),
        )

        if st.button("Remove attendance record"):
            st.session_state.attendance.pop(index)
            st.rerun()
    else:
        show_empty("No attendance records yet.")


# -----------------------------
# Assignments and homework
# -----------------------------
elif page == "Assignments & Homework":
    page_header(
        "Assignments and homework",
        "Create and track classwork, homework, projects, and tests.",
    )

    with st.form("assignment_form", clear_on_submit=True):
        title = st.text_input(
            "Assignment title",
            placeholder="For example, Chapter 2 worksheet",
        )
        kind = st.selectbox(
            "Type",
            ["Homework", "Classwork", "Project", "Test"],
        )
        due_date = st.date_input("Due date", value=date.today())
        details = st.text_area("Instructions or notes (optional)")

        submitted = st.form_submit_button(
            "Add assignment",
            type="primary",
        )

    if submitted:
        if not title.strip():
            st.error("Enter an assignment title first.")
        else:
            st.session_state.assignments.append({
                "Title": title.strip(),
                "Type": kind,
                "Due date": str(due_date),
                "Details": details.strip(),
            })
            st.success("Assignment added.")
            st.rerun()

    st.markdown(
        '<div class="section-heading">Assignment list</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.assignments:
        st.dataframe(
            pd.DataFrame(st.session_state.assignments),
            use_container_width=True,
            hide_index=True,
        )

        index = st.selectbox(
            "Select an assignment to remove",
            range(len(st.session_state.assignments)),
            format_func=lambda i: (
                f'{st.session_state.assignments[i]["Title"]} '
                f'({st.session_state.assignments[i]["Due date"]})'
            ),
        )

        if st.button("Remove selected assignment"):
            st.session_state.assignments.pop(index)
            st.rerun()
    else:
        show_empty("No assignments or homework have been created yet.")


# -----------------------------
# Student marks
# -----------------------------
elif page == "Student Marks":
    page_header(
        "Student marks",
        "Record assessment scores and review student performance.",
    )

    if not st.session_state.students:
        st.info("Add students first, then record their marks.")
    else:
        with st.form("marks_form", clear_on_submit=True):
            student = st.selectbox(
                "Student",
                st.session_state.students,
            )
            assessment = st.text_input(
                "Assessment name",
                placeholder="For example, Mathematics test",
            )
            score = st.number_input(
                "Score earned",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )
            maximum = st.number_input(
                "Maximum score",
                min_value=1.0,
                value=100.0,
                step=1.0,
            )
            assessment_date = st.date_input(
                "Assessment date",
                value=date.today(),
            )

            submitted = st.form_submit_button(
                "Save marks",
                type="primary",
            )

        if submitted:
            if not assessment.strip():
                st.error("Enter an assessment name first.")
            elif score > maximum:
                st.error("The score cannot exceed the maximum score.")
            else:
                percentage = round(score / maximum * 100, 2)

                st.session_state.marks.append({
                    "Student": student,
                    "Assessment": assessment.strip(),
                    "Score": score,
                    "Maximum score": maximum,
                    "Percentage": percentage,
                    "Date": str(assessment_date),
                })

                st.success("Marks saved.")
                st.rerun()

    st.markdown(
        '<div class="section-heading">Marks record</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.marks:
        df = pd.DataFrame(st.session_state.marks)
        st.dataframe(
            df.sort_values("Date", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

        average = round(
            sum(row["Percentage"] for row in st.session_state.marks)
            / len(st.session_state.marks),
            2,
        )
        st.metric("Average recorded percentage", f"{average}%")

        index = st.selectbox(
            "Select a marks record to remove",
            range(len(st.session_state.marks)),
            format_func=lambda i: (
                f'{st.session_state.marks[i]["Student"]} — '
                f'{st.session_state.marks[i]["Assessment"]} — '
                f'{st.session_state.marks[i]["Percentage"]}%'
            ),
        )

        if st.button("Remove selected marks record"):
            st.session_state.marks.pop(index)
            st.rerun()
    else:
        show_empty("No marks have been recorded yet.")


# -----------------------------
# Export data
# -----------------------------
elif page == "Export Data":
    page_header(
        "Export data",
        "Preview and download your class records as CSV files.",
    )

    exports = [
        (
            "Students",
            pd.DataFrame(
                st.session_state.students,
                columns=["Student"],
            ),
            "students.csv",
        ),
        (
            "Attendance",
            pd.DataFrame(st.session_state.attendance),
            "attendance.csv",
        ),
        (
            "Assignments and homework",
            pd.DataFrame(st.session_state.assignments),
            "assignments_homework.csv",
        ),
        (
            "Student marks",
            pd.DataFrame(st.session_state.marks),
            "student_marks.csv",
        ),
    ]

    for label, df, filename in exports:
        st.markdown(
            f'<div class="section-heading">{label}</div>',
            unsafe_allow_html=True,
        )

        if df.empty:
            st.caption("No records available to export yet.")
        else:
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                label=f"Download {filename}",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=filename,
                mime="text/csv",
                key=f"download_{filename}",
            )

    st.info(
        "This version stores data in the active Streamlit session only. "
        "Download your CSV files before the session ends if you need "
        "a permanent copy."
    )
