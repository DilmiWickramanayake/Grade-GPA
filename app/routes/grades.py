from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Student, Subject, Grade

grades_bp = Blueprint('grades', __name__, url_prefix='/grades')


@grades_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_grade():
    students = Student.query.order_by(Student.last_name).all()
    subjects = Subject.query.order_by(Subject.code).all()

    preselect_student = request.args.get('student_id', '')

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject_id = request.form.get('subject_id')
        letter_grade = request.form.get('letter_grade', '').strip()
        semester = request.form.get('semester', '').strip()

        if not all([student_id, subject_id, letter_grade, semester]):
            flash('All fields are required.', 'danger')
        elif letter_grade not in Grade.GRADE_POINTS:
            flash('Invalid grade.', 'danger')
        else:
            existing = Grade.query.filter_by(
                student_id=student_id, subject_id=subject_id, semester=semester).first()
            if existing:
                existing.letter_grade = letter_grade
                flash('Grade updated.', 'success')
            else:
                grade = Grade(student_id=student_id, subject_id=subject_id,
                              letter_grade=letter_grade, semester=semester)
                db.session.add(grade)
                flash('Grade added.', 'success')
            db.session.commit()
            return redirect(url_for('students.detail', student_id=student_id))

    return render_template('grades/form.html', students=students, subjects=subjects,
                           grade_options=list(Grade.GRADE_POINTS.keys()),
                           preselect_student=preselect_student)


@grades_bp.route('/<int:grade_id>/delete', methods=['POST'])
@login_required
def delete_grade(grade_id):
    grade = db.session.get(Grade, grade_id)
    if not grade:
        flash('Grade not found.', 'danger')
        return redirect(url_for('students.list_students'))
    student_id = grade.student_id
    db.session.delete(grade)
    db.session.commit()
    flash('Grade removed.', 'success')
    return redirect(url_for('students.detail', student_id=student_id))


@grades_bp.route('/subjects', methods=['GET', 'POST'])
@login_required
def subjects():
    all_subjects = Subject.query.order_by(Subject.code).all()
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        name = request.form.get('name', '').strip()
        credit_hours = request.form.get('credit_hours', 3)
        if not all([code, name]):
            flash('Code and name are required.', 'danger')
        elif Subject.query.filter_by(code=code).first():
            flash('Subject code already exists.', 'danger')
        else:
            subject = Subject(code=code, name=name, credit_hours=int(credit_hours))
            db.session.add(subject)
            db.session.commit()
            flash(f'Subject {code} added.', 'success')
            return redirect(url_for('grades.subjects'))
    return render_template('grades/subjects.html', subjects=all_subjects)
