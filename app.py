from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import Admin, Student, db # Correct import
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = ''  # Used for session management and flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'  # Connect to your database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Initialize SQLAlchemy with the app
migrate = Migrate(app, db)  # Link Flask app and SQLAlchemy database to Flask-Migrate


# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the Admin table for the provided username
        admin = Admin.query.filter_by(username=username).first()

        # Check if admin exists and password matches
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('admin_login.html')

# Admin Dashboard Route
@app.route('/admin/dashboard')
def admin_dashboard():
    # Ensure the admin is logged in, otherwise redirect to login
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    return render_template('admin_dashboard.html')

# Student login route
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        registration_number = request.form.get('registration_number')
        password = request.form.get('password')

        if not registration_number or not password:
            flash('All fields are required!', 'warning')
            return redirect(url_for('student_login'))

        # Query the students table
        student = Student.query.filter_by(registration_number=registration_number).first()

        if student and student.check_password(password):
            session['student_id'] = student.id
            flash(f'Welcome, {student.first_name}!', 'success')
            return redirect(url_for('student_dashboard'))  # Redirect to student dashboard
        else:
            flash('Invalid registration number or password', 'danger')

    return render_template('student_login.html')

# Student Dashboard Route
@app.route('/student/dashboard')
def student_dashboard():
    # Ensure the student is logged in, otherwise redirect to login
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    return render_template('student_dashboard.html')

# Logout route (for both Admin and Student)
@app.route('/logout')
def logout():
    session.clear()  # Clear session to logout
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Student registration route
@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        registration_number = request.form.get('registration_number')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        address = request.form.get('address')
        password = request.form.get('password')

        if not registration_number or not first_name or not last_name or not email or not password:
            flash('All fields are required!', 'warning')
            return redirect(url_for('student_register'))

        # Check if student already exists
        existing_student = Student.query.filter_by(registration_number=registration_number).first()
        if existing_student:
            flash('Student already exists', 'danger')
            return redirect(url_for('student_register'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create the new student
        new_student = Student(
            registration_number=registration_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            password_hash=hashed_password
        )

        # Add the new student to the database
        db.session.add(new_student)
        db.session.commit()

        flash('Student registered successfully!', 'success')
        return redirect(url_for('student_login'))

    return render_template('student_register.html')

# Create the database tables if not created
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    # Enable debugging and run the Flask app
    app.run(debug=True)
