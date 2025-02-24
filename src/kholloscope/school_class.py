"""Module that handles the definition of what constitutes a class."""

from dataclasses import dataclass


@dataclass
class Student:
    """Define mandatory fields that constitute a student."""

    first_name: str
    last_name: str
    work_group: int
    kholle_group: int
    language_1: str
    language_2: str


@dataclass
class Teacher:
    """Define mandatory fields that constitute a teacher."""

    first_name: str
    last_name: str
    subject: str
    availability: dict[int, tuple[float, float]]


@dataclass
class school_class:
    """Define mandatory fields that constitutes a class."""

    teachers: dict[str, list[Teacher]]
    students: list[Student]
    common_busy_windows: list[dict[int, tuple[float, float]]]
    language_busy_windows: list[dict[str, tuple[float, float]]]
    td_busy_windows: list[dict[int, tuple[float, float]]]

    def __post_init__(self):
        """Infer kholle groups from student lists and check their validity."""
        self.kholles_groups = self._compute_kholle_groups()
        self._assert_kholle_groups_validity()

    def _compute_kholle_groups(self) -> dict[int, list[Student]]:
        kholles_groups: dict[int, list[Student]] = {}
        for student in self.students:
            kholle_group = kholles_groups.get(student.kholle_group, [])
            kholles_groups[student.kholle_group] = kholle_group.append(Student)
        return kholles_groups

    def _assert_kholle_groups_validity(self):
        for kholle_group_students in self.kholles_groups.values():
            # all students within a group are in the same work group
            assert len({student.work_group for student in kholle_group_students}) == 1

            # all students within a group study the same languages
            assert len({student.language_1 for student in kholle_group_students}) == 1
            assert len({student.language_2 for student in kholle_group_students}) == 1

            assert len(kholle_group_students) <= 3
            assert len(kholle_group_students) >= 1
