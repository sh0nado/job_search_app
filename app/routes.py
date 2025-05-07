from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from app import app, db
from app.forms import LoginForm, RegistrationForm, UserProfileForm, SkillsSelectionForm
from app.models import User, Skill, SkillCategory
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', year=datetime.now().year)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        flash('You have been logged in successfully!', 'success')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, year=datetime.now().year)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, year=datetime.now().year)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfileForm(current_user.email)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('profile.html', form=form, title='Profile', year=datetime.now().year)

@app.route('/skills', methods=['GET', 'POST'])
@login_required
def skills():
    form = SkillsSelectionForm()
    
    # Get all skills grouped by category
    categories = SkillCategory.query.all()
    skills_by_category = []
    
    # Collect all skills for the choices field
    all_skills = Skill.query.all()
    form.skills.choices = [(skill.id, skill.name) for skill in all_skills]
    
    for category in categories:
        category_skills = Skill.query.filter_by(category_id=category.id).all()
        if category_skills:
            skills_by_category.append((category, category_skills))
    
    # Handle form submission
    if form.validate_on_submit():
        selected_skill_ids = form.skills.data
        
        # Get the selected skills
        selected_skills = Skill.query.filter(Skill.id.in_(selected_skill_ids)).all()
        
        # Update user's skills
        current_user.skills = selected_skills
        db.session.commit()
        
        flash('Your skills have been updated!', 'success')
        return redirect(url_for('profile'))
    
    # Pre-select user's existing skills
    if request.method == 'GET' and current_user.skills:
        form.skills.data = [skill.id for skill in current_user.skills]
    
    user_skills = current_user.skills
    
    return render_template('skills.html', 
                          form=form, 
                          skills_by_category=skills_by_category,
                          user_skills=user_skills,
                          title='Manage Skills',
                          year=datetime.now().year) 