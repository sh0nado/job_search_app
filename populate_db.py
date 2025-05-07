from app import app, db
from app.models import User, SkillCategory, Skill, Job
import random

def add_sample_data():
    """Add sample data to the database for testing"""
    print("Adding sample data to the database...")
    
    # Delete existing data
    Job.query.delete()
    Skill.query.delete()
    SkillCategory.query.delete()
    User.query.delete()
    db.session.commit()
    
    # Add sample users
    users = [
        {'username': 'john', 'email': 'john@example.com', 'password': 'cat123', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'jane', 'email': 'jane@example.com', 'password': 'dog123', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'bob', 'email': 'bob@example.com', 'password': 'fish123', 'first_name': 'Bob', 'last_name': 'Johnson'},
    ]
    
    for user_data in users:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        user.set_password(user_data['password'])
        db.session.add(user)
    
    db.session.commit()
    print(f"Added {len(users)} users")
    
    # Add skill categories
    categories = [
        {'name': 'Programming Languages'},
        {'name': 'Frameworks'},
        {'name': 'Databases'},
        {'name': 'Soft Skills'},
        {'name': 'Tools'},
    ]
    
    db_categories = {}
    for cat_data in categories:
        category = SkillCategory(name=cat_data['name'])
        db.session.add(category)
        db_categories[cat_data['name']] = category
    
    db.session.commit()
    print(f"Added {len(categories)} skill categories")
    
    # Add skills
    skills_data = [
        {'name': 'Python', 'description': 'Python programming language', 'category': 'Programming Languages'},
        {'name': 'JavaScript', 'description': 'JavaScript programming language', 'category': 'Programming Languages'},
        {'name': 'Java', 'description': 'Java programming language', 'category': 'Programming Languages'},
        {'name': 'C++', 'description': 'C++ programming language', 'category': 'Programming Languages'},
        
        {'name': 'Flask', 'description': 'Python web framework', 'category': 'Frameworks'},
        {'name': 'Django', 'description': 'Python web framework', 'category': 'Frameworks'},
        {'name': 'React', 'description': 'JavaScript UI library', 'category': 'Frameworks'},
        {'name': 'Angular', 'description': 'JavaScript framework', 'category': 'Frameworks'},
        
        {'name': 'SQL', 'description': 'Structured Query Language', 'category': 'Databases'},
        {'name': 'MongoDB', 'description': 'NoSQL database', 'category': 'Databases'},
        {'name': 'PostgreSQL', 'description': 'Relational database', 'category': 'Databases'},
        
        {'name': 'Communication', 'description': 'Effective communication skills', 'category': 'Soft Skills'},
        {'name': 'Teamwork', 'description': 'Ability to work in a team', 'category': 'Soft Skills'},
        {'name': 'Problem Solving', 'description': 'Analytical thinking and problem solving', 'category': 'Soft Skills'},
        
        {'name': 'Git', 'description': 'Version control system', 'category': 'Tools'},
        {'name': 'Docker', 'description': 'Containerization platform', 'category': 'Tools'},
        {'name': 'CI/CD', 'description': 'Continuous Integration and Deployment', 'category': 'Tools'},
    ]
    
    db_skills = {}
    for skill_data in skills_data:
        skill = Skill(
            name=skill_data['name'],
            description=skill_data['description'],
            category=db_categories[skill_data['category']]
        )
        db.session.add(skill)
        db_skills[skill_data['name']] = skill
    
    db.session.commit()
    print(f"Added {len(skills_data)} skills")
    
    # Add jobs
    jobs_data = [
        {
            'title': 'Python Developer',
            'company': 'Tech Solutions Inc.',
            'description': 'We are looking for a Python developer to join our team.',
            'location': 'New York, NY',
            'skills': ['Python', 'Flask', 'SQL', 'Git', 'Communication']
        },
        {
            'title': 'Full Stack Developer',
            'company': 'WebDev Co.',
            'description': 'Join our team as a full stack developer working on web applications.',
            'location': 'San Francisco, CA',
            'skills': ['JavaScript', 'React', 'Python', 'MongoDB', 'Git', 'Teamwork']
        },
        {
            'title': 'Data Engineer',
            'company': 'Data Insights',
            'description': 'Looking for a data engineer to work on data pipelines and infrastructure.',
            'location': 'Boston, MA',
            'skills': ['Python', 'SQL', 'PostgreSQL', 'Problem Solving', 'Docker']
        },
        {
            'title': 'Frontend Developer',
            'company': 'UI Wizards',
            'description': 'Create beautiful and responsive user interfaces for our clients.',
            'location': 'Austin, TX',
            'skills': ['JavaScript', 'React', 'Angular', 'Communication', 'Teamwork']
        },
        {
            'title': 'DevOps Engineer',
            'company': 'Cloud Systems',
            'description': 'Help us build and maintain our cloud infrastructure.',
            'location': 'Seattle, WA',
            'skills': ['Python', 'Docker', 'CI/CD', 'Git', 'Problem Solving']
        }
    ]
    
    for job_data in jobs_data:
        job = Job(
            title=job_data['title'],
            company=job_data['company'],
            description=job_data['description'],
            location=job_data['location']
        )
        for skill_name in job_data['skills']:
            job.skills.append(db_skills[skill_name])
        db.session.add(job)
    
    db.session.commit()
    print(f"Added {len(jobs_data)} jobs")
    
    # Assign random skills to users
    users = User.query.all()
    all_skills = list(Skill.query.all())
    
    for user in users:
        # Assign 5-8 random skills to each user
        num_skills = random.randint(5, 8)
        selected_skills = random.sample(all_skills, num_skills)
        user.skills = selected_skills
    
    db.session.commit()
    print("Assigned random skills to users")
    print("Database has been populated with sample data!")

if __name__ == '__main__':
    with app.app_context():
        add_sample_data() 