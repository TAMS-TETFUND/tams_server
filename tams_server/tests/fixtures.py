from db.models import Semester


faculty_fixture = {
    "id": 1,
    "name": "Engineering"
}
academic_session_fixture = {
    "id": 1,
    "session": "2020/2021"
}

department_fixture = {
    "id": 1,
    "name": "Electronic Engineering",
    "faculty_id": 1,
    "alias": "ECE"
}

department_api_fixture = {
    "id": 1,
    "name": "Electronic Engineering",
    "faculty": 1,
    "alias": "ECE"
}
staff_title_fixture = {
        "id": 1,
        "title_full": "Professor",
        "title": "Prof"
}

staff_fixture = {
    "id": 1,
    "department_id": 1,
    "username": "SS.4321",
    "staff_titles": [1],
    "password": "password",
    "first_name": "John",
    "last_name": "Obi",
    "email": "",
    "other_names": "Mikel",
    "staff_number": "SS.4321"
}

staff_api_fixture = {
    "id": 1,
    "department": 1,
    "username": "SS.4321",
    "staff_titles": [1],
    "password": "password",
    "first_name": "John",
    "last_name": "Obi",
    "email": "",
    "other_names": "Mikel",
    "staff_number": "SS.4321"
}

course_fixture = {
    "id": 1,
    "code": "ECE 371",
    "title": "System Programming",
    "level_of_study":1,
    "department_id":1,
    "unit_load":3,
    "semester": Semester.FIRST
}

course_api_fixture = {
    "id": 1,
    "code": "ECE 371",
    "title": "System Programming",
    "level_of_study":1,
    "department":1,
    "unit_load":3,
    "semester": Semester.FIRST
}

course_registration_fixture = {
    "id": 1,
    "session_id": 1,
    "course_id": 1,
    "student_id": 1,
    "semester": Semester.FIRST
}

course_registration_api_fixture = {
    "id": 1,
    "session": 1,
    "course": 1,
    "student": 1,
    "semester": Semester.FIRST
}
student_fixture = {
    "id": 1,
    "department_id": 1,
    "reg_number": "2020/123456",
    "first_name": "John",
    "last_name": "Doe",
    "possible_grad_yr": 2025,
    "admission_status": 1,
    "level_of_study": 2,
    "sex": 1
}

student_api_fixture = {
    "id": 1,
    "department": 1,
    "reg_number": "2020/123456",
    "first_name": "John",
    "last_name": "Doe",
    "possible_grad_yr": 2025,
    "admission_status": 1,
    "level_of_study": 2,
    "sex": 1
}