from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Student

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    students = Student.query.all()
    total_students = len(students)
    avg_gpa = round(sum(s.gpa for s in students) / total_students, 2) if total_students else 0.0
    top_students = sorted(students, key=lambda s: s.gpa, reverse=True)[:5]
    high_gpa = sum(1 for s in students if s.gpa >= 3.5)
    return render_template('index.html',
                           total_students=total_students,
                           avg_gpa=avg_gpa,
                           top_students=top_students,
                           high_gpa=high_gpa)
