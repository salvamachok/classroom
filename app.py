import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Class Monitor",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Class Monitor")
st.caption("Attendance • Homework • Assignments • Student Marks")

# Temporary storage: data lasts only for the current session.
for key in ["students", "attendance", "assignments", "marks"]:
    if key not in st.session_state:
        st.session_state[key] = []

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a section",
    [
        "Dashboard",
        "Students",
        "Attendance",
        "Assignments & Homework",
        "Student Marks",
        "Export Data",
    ],
)

students = st.session_state.students
attendance = st.session_state.attendance
assignments = st.session_state.assignments
marks = st.session_state.marks


def show_table(rows):
    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No records yet.")


if page == "Dashboard":
    st.subheader("Class Dashboard")

    a, b, c, d = st.columns(4)
    a.metric("Students", len(students))
    b.metric("Attendance records", len(attendance))
    c.metric("Assignments", len(assignments))
    d.metric("Marks recorded", len(marks))

    st.subheader("Students")
    show_table(students)

    st.warning(
        "This version uses temporary session storage. "
        "Download CSV backups before ending your session."
    )


elif page == "Students":
    st.subheader("Manage Students")

    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("Student's full name")
        student_id = st.text_input("Student ID (optional)")
        student_class = st.text_input("Class or stream (optional)")
        submitted = st.form_submit_button("Add Student")

        if submitted:
            name = name.strip()

            if not name:
                st.error("Enter the student's name.")
            elif any(
                s["name"].casefold() == name.casefold()
                for s in students
            ):
                st.error("That student is already listed.")
            else:
                st.session_state.students.append({
                    "student_id": student_id.strip()
                    or f"S{len(students) + 1:03d}",
                    "name": name,
                    "class": student_class.strip(),
                })
                st.success(f"Added {name}.")
                st.rerun()

    st.subheader("Student List")
    show_table(st.session_state.students)

    if st.session_state.students:
        names = [s["name"] for s in st.session_state.students]
        selected = st.selectbox(
            "Select student to remove",
            ["Choose a student"] + names,
        )

        if st.button("Remove Student"):
            if selected != "Choose a student":
                st.session_state.students = [
                    s for s in st.session_state.students
                    if s["name"] != selected
                ]
                st.session_state.attendance = [
                    r for r in st.session_state.attendance
                    if r["student"] != selected
                ]
                st.session_state.marks = [
                    r for r in st.session_state.marks
                    if r["student"] != selected
                ]
                st.success("Student and related records removed.")
                st.rerun()


elif page == "Attendance":
    st.subheader("Record Attendance")

    if not students:
        st.info("Add students before recording attendance.")
    else:
        attendance_date = st.date_input(
            "Attendance date",
            value=date.today(),
        )

        with st.form("attendance_form"):
            choices = {}
            for student in students:
                choices[student["name"]] = st.selectbox(
                    student["name"],
                    ["Present", "Absent", "Late", "Excused"],
                    key=f"attendance_{attendance_date}_{student['name']}",
                )

            submitted = st.form_submit_button("Save Attendance")

            if submitted:
                for name, status in choices.items():
                    existing = next(
                        (
                            r for r in st.session_state.attendance
                            if r["date"] == attendance_date.isoformat()
                            and r["student"] == name
                        ),
                        None,
                    )

                    if existing:
                        existing["status"] = status
                    else:
                        st.session_state.attendance.append({
                            "date": attendance_date.isoformat(),
                            "student": name,
                            "status": status,
                        })

                st.success("Attendance saved.")
                st.rerun()

    st.subheader("Attendance Records")
    show_table(st.session_state.attendance)


elif page == "Assignments & Homework":
    st.subheader("Assignments & Homework")

    with st.form("assignment_form", clear_on_submit=True):
        title = st.text_input("Title")
        kind = st.selectbox(
            "Type",
            ["Assignment", "Homework", "Test", "Project"],
        )
        subject = st.text_input("Subject")
        due = st.date_input("Due date", value=date.today())
        description = st.text_area("Instructions")
        submitted = st.form_submit_button("Add Item")

        if submitted:
            if not title.strip():
                st.error("Enter a title.")
            else:
                st.session_state.assignments.append({
                    "title": title.strip(),
                    "type": kind,
                    "subject": subject.strip(),
                    "due_date": due.isoformat(),
                    "description": description.strip(),
                })
                st.success("Item added.")
                st.rerun()

    st.subheader("All Assignments and Homework")
    show_table(st.session_state.assignments)

    if st.session_state.assignments:
        titles = [
            a["title"] for a in st.session_state.assignments
        ]
        selected = st.selectbox(
            "Select item to remove",
            ["Choose an item"] + titles,
        )
        if st.button("Remove Item"):
            if selected != "Choose an item":
                st.session_state.assignments = [
                    a for a in st.session_state.assignments
                    if a["title"] != selected
                ]
                st.rerun()


elif page == "Student Marks":
    st.subheader("Record Student Marks")

    if not students:
        st.info("Add students before recording marks.")
    else:
        with st.form("marks_form", clear_on_submit=True):
            student = st.selectbox(
                "Student",
                [s["name"] for s in students],
            )
            assessment = st.text_input("Subject or assessment")
            score = st.number_input(
                "Score obtained",
                min_value=0.0,
                value=0.0,
            )
            maximum = st.number_input(
                "Maximum possible score",
                min_value=1.0,
                value=100.0,
            )
            mark_date = st.date_input(
                "Assessment date",
                value=date.today(),
            )
            submitted = st.form_submit_button("Save Mark")

            if submitted:
                if not assessment.strip():
                    st.error("Enter the subject or assessment.")
                elif score > maximum:
                    st.error("Score cannot exceed the maximum.")
                else:
                    st.session_state.marks.append({
                        "student": student,
                        "assessment": assessment.strip(),
                        "score": score,
                        "maximum": maximum,
                        "percentage": round(
                            score / maximum * 100, 2
                        ),
                        "date": mark_date.isoformat(),
                    })
                    st.success("Mark saved.")
                    st.rerun()

    st.subheader("Recorded Marks")
    show_table(st.session_state.marks)

    if st.session_state.marks:
        percentages = [
            m["percentage"] for m in st.session_state.marks
        ]
        st.metric(
            "Average percentage",
            f"{sum(percentages) / len(percentages):.1f}%",
        )


elif page == "Export Data":
    st.subheader("Download Backups")

    datasets = [
        ("students", "students.csv"),
        ("attendance", "attendance.csv"),
        ("assignments", "assignments_homework.csv"),
        ("marks", "student_marks.csv"),
    ]

    for key, filename in datasets:
        rows = st.session_state[key]
        if rows:
            st.download_button(
                f"Download {filename}",
                data=pd.DataFrame(rows).to_csv(
                    index=False
                ).encode("utf-8"),
                file_name=filename,
                mime="text/csv",
                key=f"download_{key}",
            )
        else:
            st.caption(f"No {key} data to export yet.")

st.sidebar.divider()
st.sidebar.caption("No login • No Supabase")
