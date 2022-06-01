from db.models import Semester


faculty_fixture = {
    "id": 1,
    "name": "Engineering"
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
    "code": "ECE 371",
    "title": "System Programming",
    "level_of_study":1,
    "department_id":1,
    "unit_load":3,
    "semester": Semester.FIRST
}

course_api_fixture = {
    "code": "ECE 371",
    "title": "System Programming",
    "level_of_study":1,
    "department":1,
    "unit_load":3,
    "semester": Semester.FIRST
}