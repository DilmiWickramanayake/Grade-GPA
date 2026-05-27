import pytest
from app import create_app, db as _db
from app.models import User, Student, Subject, Grade


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        WTF_CSRF_ENABLED=False,
        SECRET_KEY='test-secret',
    )
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def clean_db(app):
    """Wipe all rows after every test so tests are fully isolated."""
    yield
    with app.app_context():
        _db.session.rollback()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_user(db):
    user = User(username='testadmin')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_client(client, admin_user):
    client.post('/login', data={'username': 'testadmin', 'password': 'password123'},
                follow_redirects=False)
    return client


@pytest.fixture
def sample_student(db):
    student = Student(student_id='S001', first_name='Alice', last_name='Smith',
                      email='alice@test.com')
    db.session.add(student)
    db.session.commit()
    return student


@pytest.fixture
def sample_subject(db):
    subject = Subject(code='CS101', name='Intro to CS', credit_hours=3)
    db.session.add(subject)
    db.session.commit()
    return subject


@pytest.fixture
def sample_grade(db, sample_student, sample_subject):
    grade = Grade(student_id=sample_student.id, subject_id=sample_subject.id,
                  letter_grade='A', semester='Fall 2024')
    db.session.add(grade)
    db.session.commit()
    return grade
