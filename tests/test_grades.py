"""Tests for grade and subject routes."""
from app.models import Grade, Subject


class TestAddGradeRoute:
    def test_requires_login(self, client):
        r = client.get('/grades/add', follow_redirects=False)
        assert r.status_code == 302

    def test_form_loads(self, auth_client):
        r = auth_client.get('/grades/add')
        assert r.status_code == 200
        assert b'Add Grade' in r.data

    def test_form_shows_hint_when_no_subjects(self, auth_client):
        r = auth_client.get('/grades/add')
        assert b'Add subjects first' in r.data

    def test_add_grade_success(self, auth_client, db, sample_student, sample_subject):
        r = auth_client.post('/grades/add', data={
            'student_id': str(sample_student.id),
            'subject_id': str(sample_subject.id),
            'letter_grade': 'B+',
            'semester': 'Spring 2025',
        }, follow_redirects=True)
        assert r.status_code == 200
        grade = Grade.query.filter_by(student_id=sample_student.id,
                                      subject_id=sample_subject.id).first()
        assert grade is not None
        assert grade.letter_grade == 'B+'

    def test_add_grade_updates_existing(self, auth_client, db, sample_student,
                                        sample_subject, sample_grade):
        r = auth_client.post('/grades/add', data={
            'student_id': str(sample_student.id),
            'subject_id': str(sample_subject.id),
            'letter_grade': 'C',
            'semester': 'Fall 2024',
        }, follow_redirects=True)
        assert r.status_code == 200
        db.session.refresh(sample_grade)
        assert sample_grade.letter_grade == 'C'

    def test_add_grade_missing_fields(self, auth_client, sample_student, sample_subject):
        r = auth_client.post('/grades/add', data={
            'student_id': str(sample_student.id),
            'subject_id': '',
            'letter_grade': 'A',
            'semester': '',
        }, follow_redirects=True)
        assert b'required' in r.data

    def test_add_grade_invalid_letter(self, auth_client, sample_student, sample_subject):
        r = auth_client.post('/grades/add', data={
            'student_id': str(sample_student.id),
            'subject_id': str(sample_subject.id),
            'letter_grade': 'Z',
            'semester': 'Fall 2024',
        }, follow_redirects=True)
        assert b'Invalid grade' in r.data

    def test_preselect_student_from_query_param(self, auth_client, sample_student):
        r = auth_client.get(f'/grades/add?student_id={sample_student.id}')
        assert b'selected' in r.data


class TestDeleteGradeRoute:
    def test_delete_grade(self, auth_client, db, sample_grade):
        grade_id = sample_grade.id
        r = auth_client.post(f'/grades/{grade_id}/delete', follow_redirects=True)
        assert r.status_code == 200
        assert db.session.get(Grade, grade_id) is None

    def test_delete_missing_grade_redirects(self, auth_client):
        r = auth_client.post('/grades/9999/delete', follow_redirects=True)
        assert r.status_code == 200


class TestSubjectsRoute:
    def test_subjects_page_loads(self, auth_client):
        r = auth_client.get('/grades/subjects')
        assert r.status_code == 200
        assert b'Subjects' in r.data

    def test_add_subject_success(self, auth_client, db):
        r = auth_client.post('/grades/subjects', data={
            'code': 'PH101',
            'name': 'Physics',
            'credit_hours': '4',
        }, follow_redirects=True)
        assert r.status_code == 200
        subj = Subject.query.filter_by(code='PH101').first()
        assert subj is not None
        assert subj.credit_hours == 4

    def test_add_subject_code_uppercased(self, auth_client, db):
        auth_client.post('/grades/subjects', data={
            'code': 'cs999',
            'name': 'Lower Case Code',
            'credit_hours': '3',
        }, follow_redirects=True)
        assert Subject.query.filter_by(code='CS999').first() is not None

    def test_add_duplicate_subject_code(self, auth_client, sample_subject):
        r = auth_client.post('/grades/subjects', data={
            'code': 'CS101',
            'name': 'Duplicate',
            'credit_hours': '3',
        }, follow_redirects=True)
        assert b'already exists' in r.data

    def test_add_subject_missing_name(self, auth_client):
        r = auth_client.post('/grades/subjects', data={
            'code': 'XX000',
            'name': '',
            'credit_hours': '3',
        }, follow_redirects=True)
        assert b'required' in r.data

    def test_existing_subjects_shown(self, auth_client, sample_subject):
        r = auth_client.get('/grades/subjects')
        assert b'CS101' in r.data
        assert b'Intro to CS' in r.data
