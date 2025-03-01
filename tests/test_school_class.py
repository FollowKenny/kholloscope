import pytest

from kholloscope.school_class import SchoolClass, Student, Teacher


@pytest.fixture
def some_student():
    def _some_student(
        id=0,
        first_name="John",
        last_name="Doe",
        work_group=1,
        kholle_group=1,
        language_1="spanish",
        language_2="english",
    ) -> Student:
        return Student(
            id, first_name, last_name, work_group, kholle_group, language_1, language_2
        )

    return _some_student


@pytest.fixture
def some_teacher():
    def _some_teacher(
        id=0,
        first_name="John",
        last_name="Doe",
        subject="maths",
        availability=None,
    ) -> Teacher:
        return Teacher(id, first_name, last_name, subject, availability)

    return _some_teacher


def test_school_class_missing_teachers(some_student):
    with pytest.raises(ValueError):
        SchoolClass(None, [some_student()], None, None, None)


def test_school_class_missing_students(some_teacher):
    with pytest.raises(ValueError):
        SchoolClass([some_teacher()], None, None, None, None)


def test_school_class_simple_case(some_student, some_teacher):
    school_class = SchoolClass(
        [some_teacher()],
        [some_student()],
        None,
        None,
        None,
    )
    assert school_class.kholles_groups == {1: [some_student()]}


@pytest.mark.parametrize(
    "students_params",
    [{"work_group": 2}, {"language_1": "english"}, {"language_2": "spanish"}],
)
def test_kholle_groups_consistency(some_student, some_teacher, students_params):
    students = [some_student(), some_student(**students_params)]
    with pytest.raises(ValueError):
        SchoolClass([some_teacher()], students, None, None, None)


def test_kholle_groups_limited_size(some_student, some_teacher):
    students = [some_student(), some_student(), some_student(), some_student()]
    with pytest.raises(ValueError):
        SchoolClass([some_teacher()], students, None, None, None)


def test_nominal_case(some_student, some_teacher):
    students = [
        some_student(),
        some_student(id=1),
        some_student(id=2),
        some_student(id=3, kholle_group=2),
        some_student(id=4, kholle_group=2),
        some_student(id=5, kholle_group=2),
        some_student(id=6, kholle_group=3),
    ]
    teachers = [
        some_teacher(),
        some_teacher(id=1),
        some_teacher(id=2, subject="physics"),
        some_teacher(id=3, subject="physics"),
    ]
    school_class = SchoolClass(teachers, students, None, None, None)

    assert {
        kholle_group: {student.id for student in students}
        for kholle_group, students in school_class.kholles_groups.items()
    } == {1: {0, 1, 2}, 2: {3, 4, 5}, 3: {6}}
