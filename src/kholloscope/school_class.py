"""Module that handles the definition of what constitutes a class."""

from dataclasses import dataclass


@dataclass
class Student:
    """Define mandatory fields that constitute a student."""

    id: int
    first_name: str
    last_name: str
    work_group: int
    kholle_group: int
    language_1: str
    language_2: str


@dataclass
class Teacher:
    """Define mandatory fields that constitute a teacher."""

    id: int
    first_name: str
    last_name: str
    subject: str
    availability: dict[int, tuple[float, float]]


@dataclass
class SchoolClass:
    """Define mandatory fields that constitutes a class."""

    teachers: dict[str, list[Teacher]]
    students: list[Student]
    common_busy_windows: list[dict[int, tuple[float, float]]]
    language_busy_windows: list[dict[str, tuple[float, float]]]
    td_busy_windows: list[dict[int, tuple[float, float]]]

    def __post_init__(self):
        """Infer kholle groups from student lists and check their validity."""
        if not self.teachers:
            raise ValueError("A school class cannot be initialized without teachers")
        if not self.students:
            raise ValueError("A school class cannot be initialized without students")
        self.kholles_groups = self._compute_kholle_groups()
        self._check_kholle_groups_validity()

    def _compute_kholle_groups(self) -> dict[int, list[Student]]:
        kholles_groups: dict[int, list[Student]] = {}
        for student in self.students:
            kholle_group = kholles_groups.get(student.kholle_group, [])
            kholles_groups[student.kholle_group] = kholle_group + [student]
        return kholles_groups

    def _check_kholle_groups_validity(self):
        for kholle_group, kholle_group_students in self.kholles_groups.items():
            # all students within a group are in the same work group
            if len({student.work_group for student in kholle_group_students}) != 1:
                raise ValueError(
                    (
                        f"The students in kholle group {kholle_group} "
                        "must all belong to the same work group."
                    )
                )

            # all students within a group study the same languages
            if (
                len({student.language_1 for student in kholle_group_students}) != 1
                or len({student.language_2 for student in kholle_group_students}) != 1
            ):
                raise ValueError(
                    (
                        f"The students in kholle group {kholle_group} "
                        "must all study the same languages."
                    )
                )

            # a kholle group is made of 1-3 students
            if len(kholle_group_students) > 3:
                raise ValueError(
                    f"The kholle group {kholle_group} has too many students (3 max)."
                )
