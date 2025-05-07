from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime

# Association tables for many-to-many relationships
user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

job_skills = db.Table('job_skills',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with skills
    skills = db.relationship('Skill', secondary=user_skills, 
                            backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class SkillCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    
    # Relationship with skills
    skills = db.relationship('Skill', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return '<SkillCategory {}>'.format(self.name)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    category_id = db.Column(db.Integer, db.ForeignKey('skill_category.id'))
    
    def __repr__(self):
        return '<Skill {}>'.format(self.name)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    company = db.Column(db.String(128))
    description = db.Column(db.Text)
    location = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with skills
    skills = db.relationship('Skill', secondary=job_skills, 
                           backref=db.backref('jobs', lazy='dynamic'))
    
    def __repr__(self):
        return '<Job {}>'.format(self.title)
    
    def compatibility_score(self, user):
        """Calculate compatibility score with a user based on matching skills"""
        user_skills = set(user.skills)
        job_skills = set(self.skills)
        
        if not job_skills:
            return 0
            
        matching_skills = user_skills.intersection(job_skills)
        return (len(matching_skills) / len(job_skills)) * 100

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) 