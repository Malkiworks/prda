from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange
import sqlite3
import os
from datetime import datetime

# Initialize Flask application with secret key for CSRF protection
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Database configuration - SQLite database file path
DATABASE = 'users.db'

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Creates the database file if it doesn't exist.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return conn

def init_db():
    """
    Initialize the database by creating the users table if it doesn't exist.
    This function sets up the schema for storing user profile data.
    """
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER NOT NULL,
            bio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Flask-WTF form class for user registration with comprehensive validation
class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ])
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    age = IntegerField('Age', validators=[
        DataRequired(message='Age is required'),
        NumberRange(min=13, max=120, message='Age must be between 13 and 120')
    ])
    bio = TextAreaField('Bio', validators=[
        Length(max=500, message='Bio must be less than 500 characters')
    ])
    submit = SubmitField('Register')

# Flask-WTF form class for updating user profile (similar to registration but for updates)
class UserUpdateForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ])
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    age = IntegerField('Age', validators=[
        DataRequired(message='Age is required'),
        NumberRange(min=13, max=120, message='Age must be between 13 and 120')
    ])
    bio = TextAreaField('Bio', validators=[
        Length(max=500, message='Bio must be less than 500 characters')
    ])
    submit = SubmitField('Update Profile')

@app.route('/')
def index():
    """
    Home page route that displays all registered users.
    Retrieves user data from database and renders it dynamically.
    """
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration route that handles both GET (display form) and POST (process form).
    Validates input data and stores new user information in the database.
    """
    form = UserRegistrationForm()
    
    if form.validate_on_submit():
        # Extract validated form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        age = form.age.data
        bio = form.bio.data
        
        try:
            # Insert new user into database with error handling for duplicate emails
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO users (first_name, last_name, email, age, bio)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, age, bio))
            conn.commit()
            conn.close()
            
            flash('Registration successful! Welcome to our platform.', 'success')
            return redirect(url_for('index'))
            
        except sqlite3.IntegrityError:
            # Handle duplicate email error with user-friendly message
            flash('Email address already exists. Please use a different email.', 'error')
    
    return render_template('register.html', form=form)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    """
    Individual user profile display route.
    Retrieves and displays specific user data based on user ID.
    """
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if user is None:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    
    return render_template('profile.html', user=user)

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
    """
    User profile update route that preloads existing data into the form.
    Handles both displaying the pre-filled form and processing updates.
    """
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if user is None:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    
    form = UserUpdateForm()
    
    if form.validate_on_submit():
        # Process form submission with updated data
        try:
            conn.execute('''
                UPDATE users 
                SET first_name = ?, last_name = ?, email = ?, age = ?, bio = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (form.first_name.data, form.last_name.data, form.email.data, 
                  form.age.data, form.bio.data, user_id))
            conn.commit()
            conn.close()
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile', user_id=user_id))
            
        except sqlite3.IntegrityError:
            flash('Email address already exists. Please use a different email.', 'error')
    
    elif request.method == 'GET':
        # Pre-populate form with existing user data for editing
        form.first_name.data = user['first_name']
        form.last_name.data = user['last_name']
        form.email.data = user['email']
        form.age.data = user['age']
        form.bio.data = user['bio']
    
    conn.close()
    return render_template('update.html', form=form, user=user)

# Initialize database when application starts
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 