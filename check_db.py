from app import app, db
from app.models import User, SkillCategory, Skill, Job

def check_database():
    """Check database contents to verify sample data was properly loaded"""
    with app.app_context():
        # Check users
        users = User.query.all()
        print(f"\nFound {len(users)} users:")
        for user in users:
            print(f"  - {user.username} ({user.email}): {len(user.skills)} skills")
            
        # Check skill categories
        categories = SkillCategory.query.all()
        print(f"\nFound {len(categories)} skill categories:")
        for category in categories:
            print(f"  - {category.name}: {category.skills.count()} skills")
            
        # Check skills
        skills = Skill.query.all()
        print(f"\nFound {len(skills)} skills:")
        for skill in skills:
            print(f"  - {skill.name} ({skill.category.name})")
            
        # Check jobs
        jobs = Job.query.all()
        print(f"\nFound {len(jobs)} jobs:")
        for job in jobs:
            print(f"  - {job.title} at {job.company} ({len(job.skills)} skills required)")
            
        # Compute compatibility for a sample user with all jobs
        if users and jobs:
            sample_user = users[0]
            print(f"\nCompatibility scores for user {sample_user.username}:")
            for job in jobs:
                score = job.compatibility_score(sample_user)
                print(f"  - {job.title}: {score:.1f}% match")

if __name__ == "__main__":
    check_database() 