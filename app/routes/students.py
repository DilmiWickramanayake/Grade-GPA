from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Student

students_bp = Blueprint('students', __name__, url_prefix='/students')


@students_bp.route('/')
@login_required
def list_students():
    students = Student.query.order_by(Student.last_name).all()
    return render_template('students/list.html', students=students)


@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()

        if not all([student_id, first_name, last_name, email]):
            flash('All fields are required.', 'danger')
        elif Student.query.filter_by(student_id=student_id).first():
            flash('Student ID already exists.', 'danger')
        elif Student.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
        else:
            student = Student(student_id=student_id, first_name=first_name,
                              last_name=last_name, email=email)
            db.session.add(student)
            db.session.commit()
            flash(f'Student {student.full_name} added successfully.', 'success')
            return redirect(url_for('students.list_students'))

    return render_template('students/form.html', action='Add', student=None)


@students_bp.route('/<int:student_id>')
@login_required
def detail(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('students/detail.html', student=student)


@students_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form.get('first_name', '').strip()
        student.last_name = request.form.get('last_name', '').strip()
        student.email = request.form.get('email', '').strip()
        db.session.commit()
        flash('Student updated.', 'success')
        return redirect(url_for('students.detail', student_id=student.id))
    return render_template('students/form.html', action='Edit', student=student)


@students_bp.route('/<int:student_id>/delete', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted.', 'success')
    return redirect(url_for('students.list_students'))
