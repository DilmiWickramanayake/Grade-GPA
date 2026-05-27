"""Tests for student CRUD routes."""
from app.models import Student


class TestStudentListRoute:
    def test_requires_login(self, client):
        r = client.get('/students/', follow_redirects=False)
        assert r.status_code == 302
        assert '/login' in r.headers['Location']

    def test_lists_students(self, auth_client, sample_student):
        r = auth_client.get('/students/')
        assert r.status_code == 200
        assert b'Alice Smith' in r.data
        assert b'S001' in r.data

    def test_empty_list_shows_message(self, auth_client):
        r = auth_client.get('/students/')
        assert r.status_code == 200


class TestAddStudentRoute:
    def test_add_form_loads(self, auth_client):
        r = auth_client.get('/students/add')
        assert r.status_code == 200
        assert b'Add Student' in r.data

    def test_add_valid_student(self, auth_client, db):
        r = auth_client.post('/students/add', data={
            'student_id': 'S099',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@test.com',
        }, follow_redirects=True)
        assert r.status_code == 200
        assert Student.query.filter_by(student_id='S099').first() is not None

    def test_add_duplicate_student_id(self, auth_client, sample_student):
        r = auth_client.post('/students/add', data={
            'student_id': 'S001',
            'first_name': 'Copy',
            'last_name': 'Cat',
            'email': 'copy@test.com',
        }, follow_redirects=True)
        assert b'already exists' in r.data

    def test_add_duplicate_email(self, auth_client, sample_student):
        r = auth_client.post('/students/add', data={
            'student_id': 'S999',
            'first_name': 'Dup',
            'last_name': 'Email',
            'email': 'alice@test.com',
        }, follow_redirects=True)
        assert b'already registered' in r.data

    def test_add_missing_fields(self, auth_client):
        r = auth_client.post('/students/add', data={
            'student_id': 'S050',
            'first_name': '',
            'last_name': 'Empty',
            'email': '',
        }, follow_redirects=True)
        assert b'required' in r.data


class TestStudentDetailRoute:
    def test_detail_page_loads(self, auth_client, sample_student):
        r = auth_client.get(f'/students/{sample_student.id}')
        assert r.status_code == 200
        assert b'Alice Smith' in r.data
        assert b'S001' in r.data

    def test_detail_shows_gpa(self, auth_client, sample_student, sample_grade):
        r = auth_client.get(f'/students/{sample_student.id}')
        assert b'4.0' in r.data

    def test_detail_404_for_missing(self, auth_client):
        r = auth_client.get('/students/9999')
        assert r.status_code == 404


class TestEditStudentRoute:
    def test_edit_form_loads_with_data(self, auth_client, sample_student):
        r = auth_client.get(f'/students/{sample_student.id}/edit')
        assert r.status_code == 200
        assert b'Alice' in r.data

    def test_edit_updates_student(self, auth_client, sample_student, db):
        r = auth_client.post(f'/students/{sample_student.id}/edit', data={
            'first_name': 'Alicia',
            'last_name': 'Smith',
            'email': 'alice@test.com',
        }, follow_redirects=True)
        assert r.status_code == 200
        db.session.refresh(sample_student)
        assert sample_student.first_name == 'Alicia'


class TestDeleteStudentRoute:
    def test_delete_removes_student(self, auth_client, db):
        student = Student(student_id='SDEL', first_name='Del', last_name='Me',
                          email='delme@test.com')
        db.session.add(student)
        db.session.commit()
        sid = student.id

        r = auth_client.post(f'/students/{sid}/delete', follow_redirects=True)
        assert r.status_code == 200
        assert db.session.get(Student, sid) is None

    def test_delete_404_for_missing(self, auth_client):
        r = auth_client.post('/students/9999/delete')
        assert r.status_code == 404
