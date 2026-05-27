"""Tests for login, register, and logout routes."""


class TestLoginPage:
    def test_login_page_loads(self, client):
        r = client.get('/login')
        assert r.status_code == 200
        assert b'Sign In' in r.data
        assert b'GPA Tracker' in r.data

    def test_login_page_has_register_link(self, client):
        r = client.get('/login')
        assert b'/register' in r.data

    def test_login_valid_credentials(self, client, admin_user):
        r = client.post('/login', data={'username': 'testadmin', 'password': 'password123'},
                        follow_redirects=True)
        assert r.status_code == 200
        assert b'Dashboard' in r.data

    def test_login_wrong_password(self, client, admin_user):
        r = client.post('/login', data={'username': 'testadmin', 'password': 'wrongpass'},
                        follow_redirects=True)
        assert r.status_code == 200
        assert b'Invalid username or password' in r.data

    def test_login_unknown_user(self, client):
        r = client.post('/login', data={'username': 'nobody', 'password': 'anything'},
                        follow_redirects=True)
        assert b'Invalid username or password' in r.data

    def test_login_redirects_authenticated_user(self, auth_client):
        r = auth_client.get('/login', follow_redirects=False)
        assert r.status_code == 302

    def test_login_next_param_respected(self, client, admin_user):
        r = client.post('/login?next=%2Fstudents%2F',
                        data={'username': 'testadmin', 'password': 'password123'},
                        follow_redirects=False)
        assert r.status_code == 302
        assert '/students/' in r.headers['Location']


class TestRegisterPage:
    def test_register_page_loads(self, client):
        r = client.get('/register')
        assert r.status_code == 200
        assert b'Create Account' in r.data

    def test_register_page_has_login_link(self, client):
        r = client.get('/register')
        assert b'/login' in r.data

    def test_register_creates_user_and_redirects(self, client, db):
        r = client.post('/register', data={
            'username': 'newuser',
            'password': 'secure123',
            'confirm_password': 'secure123',
        }, follow_redirects=True)
        assert r.status_code == 200
        assert b'Dashboard' in r.data
        from app.models import User
        assert User.query.filter_by(username='newuser').first() is not None

    def test_register_password_mismatch(self, client):
        r = client.post('/register', data={
            'username': 'mismatch',
            'password': 'abc123',
            'confirm_password': 'xyz999',
        }, follow_redirects=True)
        assert b'Passwords do not match' in r.data

    def test_register_short_password(self, client):
        r = client.post('/register', data={
            'username': 'shortpw',
            'password': 'ab',
            'confirm_password': 'ab',
        }, follow_redirects=True)
        assert b'at least 6' in r.data

    def test_register_duplicate_username(self, client, admin_user):
        r = client.post('/register', data={
            'username': 'testadmin',
            'password': 'password123',
            'confirm_password': 'password123',
        }, follow_redirects=True)
        assert b'already taken' in r.data

    def test_register_empty_username(self, client):
        r = client.post('/register', data={
            'username': '',
            'password': 'password123',
            'confirm_password': 'password123',
        }, follow_redirects=True)
        assert b'required' in r.data

    def test_register_repopulates_username_on_error(self, client, admin_user):
        r = client.post('/register', data={
            'username': 'testadmin',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        assert b'testadmin' in r.data


class TestLogout:
    def test_logout_redirects_to_login(self, auth_client):
        r = auth_client.get('/logout', follow_redirects=False)
        assert r.status_code == 302
        assert '/login' in r.headers['Location']

    def test_logout_unauthenticated_redirects(self, client):
        r = client.get('/logout', follow_redirects=False)
        assert r.status_code == 302
