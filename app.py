
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Class Monitor",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- CUSTOM DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #3157D5;
    --primary-dark: #2444B5;
    --ink: #19243A;
    --muted: #78849A;
    --line: #E5EAF2;
    --background: #F5F7FB;
}

.stApp {
    background: var(--background);
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--ink);
    letter-spacing: -0.5px;
}

h1 { font-size: 2rem !important; font-weight: 800 !important; }
h2 { font-size: 1.4rem !important; font-weight: 750 !important; }
h3 { font-size: 1.05rem !important; font-weight: 700 !important; }

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

.brand {
    padding: 12px 12px 24px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 20px;
}

.brand-mark {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    background: var(--primary);
    color: white;
    border-radius: 12px;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 12px;
}

.brand-name {
    font-family: 'Manrope', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: var(--ink);
}

.brand-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-top: 4px;
}

.sidebar-label {
    color: #8993A5;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin: 20px 0 8px;
}

.hero {
    background: linear-gradient(115deg, #243FAD, #4169E8);
    padding: 28px 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 28px rgba(49,87,213,0.14);
}

.hero h2 {
    color: white !important;
    font-size: 25px !important;
    margin: 0 0 8px 0;
}

.hero p {
    color: #E2E9FF;
    margin: 0;
    font-size: 14px;
}

.eyebrow {
    color: #D6E0FF;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    margin-bottom: 10px;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(25,36,58,0.025);
}

.metric-label {
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 13px;
}

.metric-value {
    color: var(--ink);
    font-family: 'Manrope', sans-serif;
    font-size: 30px;
    font-weight: 800;
    line-height: 1.1;
}

.metric-note {
    color: var(--muted);
    font-size: 11px;
    margin-top: 8px;
}

.panel {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 20px;
    margin: 12px 0 20px;
}

.panel-title {
    font-family: 'Manrope', sans-serif;
    font-size: 16px;
    font-weight: 750;
    margin-bottom: 5px;
}

.panel-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 15px;
}

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 22px;
}

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 9px;
    font-weight: 600;
    min-height: 42px;
    transition: 0.15s ease;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: var(--primary);
    border-color: var(--primary);
}

.stButton > button:hover {
    border-color: var(--primary);
    color: var(--primary);
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    border-radius: 9px;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow: hidden;
}

hr {
    border-color: var(--line);
}

.small-muted {
    color: var(--muted);
    font-size: 12px;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }
    .hero {
        padding: 22px;
    }
    .metric-value {
        font-size: 25px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- SESSION STORAGE --------------------

for key in ["students", "attendance", "assignments", "marks"]:
    if key not in st.session_state:
        st.session_state[key] = []

students = st.session_state.students
attendance = st.session_state.attendance
assignments = st.session_state.assignments
marks = st.session_state.marks


# -------------------- HELPER FUNCTIONS --------------------

def show_table(rows):
    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No records available yet.")


def metric_card(label, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_heading(title, subtitle):
    st.markdown(f"# {title}")
    st.markdown(
        f'<p class="small-muted">{subtitle}</p>',
        unsafe_allow_html=True,
    )


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-mark">C</div>
        <div class="brand-name">Class Monitor</div>
        <div class="brand-subtitle">Classroom management</div>
    </div>
    <div class="sidebar-label">WORKSPACE</div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Main navigation",
        [
            "Dashboard",
            "Students",
            "Attendance",
            "Assignments & Homework",
            "Student Marks",
            "Export Data",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown(
        '<div class="small-muted">Classroom tools<br>No account required</div>',
        unsafe_allow_html=True,
    )


# -------------------- DASHBOARD --------------------

if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">CLASSROOM OVERVIEW</div>
        <h2>Welcome to Class Monitor</h2>
        <p>Manage your class records, track attendance and review academic progress.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("TOTAL STUDENTS", len(students), "Students registered")

    with c2:
        today_records = [
            r for r in attendance
            if r["date"] == date.today().isoformat()
        ]
        metric_card("TODAY'S RECORDS", len(today_records), "Attendance entries")

    with c3:
        metric_card("ASSIGNMENTS", len(assignments), "Items created")

    with c4:
        metric_card("MARKS RECORDED", len(marks), "Assessment entries")

    st.write("")
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown(
            '<div class="panel"><div class="panel-title">Recent attendance</div>'
            '<div class="panel-subtitle">Latest saved attendance entries</div></div>',
            unsafe_allow_html=True,
        )

        if attendance:
            recent = sorted(
                attendance,
                key=lambda r: r["date"],
                reverse=True,
            )[:8]
            show_table(recent)
        else:
            st.info("Attendance records will appear here after you record attendance.")

    with right:
        st.markdown(
            '<div class="panel"><div class="panel-title">Class summary</div>'
            '<div class="panel-subtitle">Current workspace activity</div></div>',
            unsafe_allow_html=True,
        )

        present_today = sum(
            r["status"] == "Present" for r in today_records
        )
        absent_today = sum(
            r["status"] == "Absent" for r in today_records
        )

        st.metric("Present today", present_today)
        st.metric("Absent today", absent_today)
        st.metric("Homework and assignments", len(assignments))

    st.caption(
        "This version stores records temporarily in the current session. "
        "Use Export Data to download backups."
    )


# -------------------- STUDENTS --------------------

elif page == "Students":
    page_heading(
        "Students",
        "Register students and maintain your class list.",
    )

    with st.form("student_form", clear_on_submit=True):
        st.subheader("Add a student")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full name", placeholder="Enter student's name")
            student_id = st.text_input(
                "Student ID",
                placeholder="Optional student number",
            )

        with col2:
            student_class = st.text_input(
                "Class or stream",
                placeholder="For example, Senior 4",
            )

        submitted = st.form_submit_button(
            "Add student",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            name = name.strip()

            if not name:
                st.error("Please enter the student's name.")
            elif any(
                s["name"].casefold() == name.casefold()
                for s in students
            ):
                st.error("A student with this name already exists.")
            else:
                st.session_state.students.append({
                    "student_id": student_id.strip()
                    or f"S{len(students) + 1:03d}",
                    "name": name,
                    "class": student_class.strip(),
                })
                st.success("Student added successfully.")
                st.rerun()

    st.subheader("Student directory")
    st.caption(f"{len(students)} student(s) registered")

    show_table(st.session_state.students)

    if students:
        with st.expander("Remove a student"):
            names = [s["name"] for s in students]
            selected = st.selectbox(
                "Select student",
                names,
                key="remove_student",
            )

            if st.button("Remove selected student"):
                st.session_state.students = [
                    s for s in students if s["name"] != selected
                ]
                st.session_state.attendance = [
                    r for r in attendance if r["student"] != selected
                ]
                st.session_state.marks = [
                    r for r in marks if r["student"] != selected
                ]
                st.success("Student and related attendance and marks removed.")
                st.rerun()


# -------------------- ATTENDANCE --------------------

elif page == "Attendance":
    page_heading(
        "Attendance",
        "Record and review daily student attendance.",
    )

    if not students:
        st.info("Register students before recording attendance.")
    else:
        st.markdown(
            '<div class="panel"><div class="panel-title">Daily register</div>'
            '<div class="panel-subtitle">Choose a date and record each student\'s status.</div></div>',
            unsafe_allow_html=True,
        )

        selected_date = st.date_input(
            "Attendance date",
            value=date.today(),
        )

        with st.form("attendance_form"):
            statuses = {}

            for student in students:
                previous = next(
                    (
                        r["status"] for r in attendance
                        if r["date"] == selected_date.isoformat()
                        and r["student"] == student["name"]
                    ),
                    "Present",
                )

                statuses[student["name"]] = st.selectbox(
                    student["name"],
                    ["Present", "Absent", "Late", "Excused"],
                    index=["Present", "Absent", "Late", "Excused"].index(previous),
                    key=f"status_{selected_date}_{student['name']}",
                )

            submitted = st.form_submit_button(
                "Save attendance",
                type="primary",
                use_container_width=True,
            )

            if submitted:
                for student_name, status in statuses.items():
                    existing = next(
                        (
                            r for r in st.session_state.attendance
                            if r["date"] == selected_date.isoformat()
                            and r["student"] == student_name
                        ),
                        None,
                    )

                    if existing:
                        existing["status"] = status
                    else:
                        st.session_state.attendance.append({
                            "date": selected_date.isoformat(),
                            "student": student_name,
                            "status": status,
                        })

                st.success("Attendance saved successfully.")
                st.rerun()

    st.subheader("Attendance history")

    if attendance:
        available_dates = sorted(
            {r["date"] for r in attendance},
            reverse=True,
        )

        filter_date = st.selectbox(
            "Filter by date",
            available_dates,
        )

        filtered = [
            r for r in attendance if r["date"] == filter_date
        ]

        a, b, c, d = st.columns(4)
        with a:
            metric_card("PRESENT", sum(r["status"] == "Present" for r in filtered), "Students")
        with b:
            metric_card("ABSENT", sum(r["status"] == "Absent" for r in filtered), "Students")
        with c:
            metric_card("LATE", sum(r["status"] == "Late" for r in filtered), "Students")
        with d:
            metric_card("EXCUSED", sum(r["status"] == "Excused" for r in filtered), "Students")

        st.write("")
        show_table(filtered)
    else:
        st.info("No attendance has been recorded yet.")


# -------------------- ASSIGNMENTS --------------------

elif page == "Assignments & Homework":
    page_heading(
        "Assignments & Homework",
        "Create tasks, set deadlines and review classwork.",
    )

    with st.form("assignment_form", clear_on_submit=True):
        st.subheader("Create a new item")

        title = st.text_input(
            "Title",
            placeholder="Enter assignment or homework title",
        )

        col1, col2 = st.columns(2)

        with col1:
            kind = st.selectbox(
                "Category",
                ["Assignment", "Homework", "Test", "Project"],
            )
            subject = st.text_input("Subject")

        with col2:
            due_date = st.date_input(
                "Due date",
                value=date.today(),
            )

        description = st.text_area(
            "Instructions",
            placeholder="Add details or instructions for students",
        )

        submitted = st.form_submit_button(
            "Create item",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if not title.strip():
                st.error("Please enter a title.")
            else:
                st.session_state.assignments.append({
                    "title": title.strip(),
                    "type": kind,
                    "subject": subject.strip(),
                    "due_date": due_date.isoformat(),
                    "description": description.strip(),
                })
                st.success("Item created successfully.")
                st.rerun()

    st.subheader("Classwork overview")

    if assignments:
        search = st.text_input(
            "Search by title or subject",
            placeholder="Type to filter assignments",
        )

        filtered = [
            a for a in assignments
            if search.casefold() in a["title"].casefold()
            or search.casefold() in a["subject"].casefold()
        ]

        show_table(filtered)

        with st.expander("Remove an item"):
            titles = [a["title"] for a in assignments]
            selected_title = st.selectbox(
                "Select item",
                titles,
                key="remove_assignment",
            )

            if st.button("Remove selected item"):
                st.session_state.assignments = [
                    a for a in assignments
                    if a["title"] != selected_title
                ]
                st.success("Item removed.")
                st.rerun()
    else:
        st.info("No assignments or homework have been created.")


# -------------------- STUDENT MARKS --------------------

elif page == "Student Marks":
    page_heading(
        "Student Marks",
        "Record assessment scores and review academic performance.",
    )

    if not students:
        st.info("Register students before entering marks.")
    else:
        with st.form("marks_form", clear_on_submit=True):
            st.subheader("Enter assessment result")

            student_name = st.selectbox(
                "Student",
                [s["name"] for s in students],
            )

            assessment = st.text_input(
                "Assessment or subject",
                placeholder="For example, Mathematics test",
            )

            col1, col2 = st.columns(2)

            with col1:
                score = st.number_input(
                    "Score obtained",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                )

            with col2:
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
                "Save result",
                type="primary",
                use_container_width=True,
            )

            if submitted:
                if not assessment.strip():
                    st.error("Please enter the assessment or subject.")
                elif score > maximum:
                    st.error("The score cannot exceed the maximum score.")
                else:
                    st.session_state.marks.append({
                        "student": student_name,
                        "assessment": assessment.strip(),
                        "score": score,
                        "maximum": maximum,
                        "percentage": round(score / maximum * 100, 2),
                        "date": assessment_date.isoformat(),
                    })
                    st.success("Result saved successfully.")
                    st.rerun()

    st.subheader("Results register")

    if marks:
        student_filter = st.selectbox(
            "Filter results",
            ["All students"] + [s["name"] for s in students],
        )

        filtered_marks = [
            m for m in marks
            if student_filter == "All students"
            or m["student"] == student_filter
        ]

        show_table(filtered_marks)

        if filtered_marks:
            average = sum(
                m["percentage"] for m in filtered_marks
            ) / len(filtered_marks)

            st.write("")
            metric_card(
                "AVERAGE SCORE",
                f"{average:.1f}%",
                "Based on the displayed results",
            )
    else:
        st.info("No assessment results have been recorded.")


# -------------------- EXPORTS --------------------

elif page == "Export Data":
    page_heading(
        "Export Data",
        "Download CSV copies of your current class records.",
    )

    datasets = [
        ("students", "students.csv", "Student directory"),
        ("attendance", "attendance.csv", "Attendance register"),
        ("assignments", "assignments_homework.csv", "Assignments and homework"),
        ("marks", "student_marks.csv", "Student marks"),
    ]

    for key, filename, label in datasets:
        rows = st.session_state[key]

        with st.container(border=True):
            left, right = st.columns([3, 1])

            with left:
                st.markdown(f"**{label}**")
                st.caption(f"{len(rows)} record(s) available")

            with right:
                if rows:
                    st.download_button(
                        "Download CSV",
                        data=pd.DataFrame(rows).to_csv(
                            index=False
                        ).encode("utf-8"),
                        file_name=filename,
                        mime="text/csv",
                        key=f"download_{key}",
                        use_container_width=True,
                    )
                else:
                    st.button(
                        "No data",
                        disabled=True,
                        key=f"empty_{key}",
                        use_container_width=True,
                    )

    st.warning(
        "Records are stored temporarily in the current session. "
        "Download your files before closing or refreshing the app."
    )
