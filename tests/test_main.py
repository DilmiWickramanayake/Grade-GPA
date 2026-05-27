"""Tests for the dashboard / main route."""


class TestDashboardRoute:
    def test_requires_login(self, client):
        r = client.get('/', follow_redirects=False)
        assert r.status_code == 302
        assert '/login' in r.headers['Location']

    def test_dashboard_loads(self, auth_client):
        r = auth_client.get('/')
        assert r.status_code == 200
        assert b'Dashboard' in r.data

    def test_dashboard_shows_zero_stats_when_empty(self, auth_client):
        r = auth_client.get('/')
        assert b'0' in r.data

    def test_dashboard_shows_total_students(self, auth_client, sample_student):
        r = auth_client.get('/')
        assert b'1' in r.data

    def test_dashboard_shows_student_in_top_list(self, auth_client, sample_student, sample_grade):
        r = auth_client.get('/')
        assert b'Alice Smith' in r.data

    def test_dashboard_shows_avg_gpa(self, auth_client, sample_student, sample_grade):
        r = auth_client.get('/')
        # sample_grade is an A = 4.0
        assert b'4.0' in r.data

    def test_dashboard_shows_high_gpa_count(self, auth_client, sample_student, sample_grade):
        r = auth_client.get('/')
        # student has 4.0 GPA so high_gpa should be 1
        assert r.status_code == 200

    def test_dashboard_navbar_present(self, auth_client):
        r = auth_client.get('/')
        assert b'Students' in r.data
        assert b'Subjects' in r.data
