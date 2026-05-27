"""Unit tests for database models."""
import pytest
from app.models import User, Student, Subject, Grade


class TestUserModel:
    def test_password_hashing(self, db):
        user = User(username='bob')
        user.set_password('secret')
        db.session.add(user)
        db.session.commit()

        assert user.password_hash != 'secret'
        assert user.check_password('secret') is True
        assert user.check_password('wrong') is False

    def test_username_unique(self, db):
        u1 = User(username='dupuser')
        u1.set_password('pass')
        u2 = User(username='dupuser')
        u2.set_password('pass')
        db.session.add(u1)
        db.session.commit()
        db.session.add(u2)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()


class TestStudentModel:
    def test_full_name(self, db):
        student = Student(student_id='S010', first_name='Jane', last_name='Doe',
                          email='jane@test.com')
        db.session.add(student)
        db.session.commit()
        assert student.full_name == 'Jane Doe'

    def test_gpa_no_grades(self, db):
        student = Student(student_id='S011', first_name='No', last_name='Grades',
                          email='nogrades@test.com')
        db.session.add(student)
        db.session.commit()
        assert student.gpa == 0.0

    def test_gpa_single_grade(self, db):
        student = Student(student_id='S012', first_name='One', last_name='Grade',
                          email='onegrade@test.com')
        subject = Subject(code='MA100', name='Math', credit_hours=3)
        db.session.add_all([student, subject])
        db.session.commit()
        grade = Grade(student_id=student.id, subject_id=subject.id,
                      letter_grade='A', semester='Fall 2024')
        db.session.add(grade)
        db.session.commit()
        assert student.gpa == 4.0

    def test_gpa_multiple_grades(self, db):
        student = Student(student_id='S013', first_name='Multi', last_name='Grade',
                          email='multi@test.com')
        s1 = Subject(code='MA200', name='Math 2', credit_hours=3)
        s2 = Subject(code='EN100', name='English', credit_hours=3)
        db.session.add_all([student, s1, s2])
        db.session.commit()
        # A (4.0 × 3) + B (3.0 × 3) = 21 / 6 = 3.5
        g1 = Grade(student_id=student.id, subject_id=s1.id, letter_grade='A', semester='F24')
        g2 = Grade(student_id=student.id, subject_id=s2.id, letter_grade='B', semester='F24')
        db.session.add_all([g1, g2])
        db.session.commit()
        assert student.gpa == 3.5

    def test_gpa_weighted_by_credits(self, db):
        student = Student(student_id='S014', first_name='Weight', last_name='Test',
                          email='weight@test.com')
        s1 = Subject(code='PH300', name='Physics', credit_hours=4)
        s2 = Subject(code='ART10', name='Art', credit_hours=1)
        db.session.add_all([student, s1, s2])
        db.session.commit()
        # A (4.0×4=16) + F (0.0×1=0) = 16/5 = 3.2
        g1 = Grade(student_id=student.id, subject_id=s1.id, letter_grade='A', semester='F24')
        g2 = Grade(student_id=student.id, subject_id=s2.id, letter_grade='F', semester='F24')
        db.session.add_all([g1, g2])
        db.session.commit()
        assert student.gpa == 3.2

    def test_cascade_delete_grades(self, db, sample_student, sample_grade):
        grade_id = sample_grade.id
        db.session.delete(sample_student)
        db.session.commit()
        assert db.session.get(Grade, grade_id) is None


class TestGradeModel:
    def test_grade_points_all_letters(self):
        expected = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0,
        }
        for letter, points in expected.items():
            g = Grade(letter_grade=letter)
            assert g.grade_points == points, f'{letter} should be {points}'

    def test_grade_points_unknown_returns_zero(self):
        g = Grade(letter_grade='X')
        assert g.grade_points == 0.0

    def test_credit_hours_from_subject(self, db, sample_student, sample_subject):
        grade = Grade(student_id=sample_student.id, subject_id=sample_subject.id,
                      letter_grade='B', semester='Fall 2024')
        db.session.add(grade)
        db.session.commit()
        assert grade.credit_hours == sample_subject.credit_hours
