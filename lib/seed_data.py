
from lib.db import get_db
from models.vaccine import Vaccine
from models.user import User
from models.child import Child
from models.child_vaccine import ChildVaccine
from models.reminder import Reminder
from datetime import datetime, date, timedelta

def seed_vaccines():
    """Seed the database with standard vaccine information"""
    print("Seeding vaccines...")
    
    vaccines_data = [
        {
            "name": "Hepatitis B",
            "description": "Protects against hepatitis B virus infection",
            "recommended_age_months": 0,
            "dose_number": 1,
            "is_required": True
        },
        {
            "name": "DTaP",
            "description": "Diphtheria, Tetanus, Pertussis vaccine",
            "recommended_age_months": 2,
            "dose_number": 1,
            "is_required": True
        },
        {
            "name": "Hib",
            "description": "Haemophilus influenzae type b vaccine",
            "recommended_age_months": 2,
            "dose_number": 1,
            "is_required": True
        },
        {
            "name": "IPV",
            "description": "Inactivated Poliovirus vaccine",
            "recommended_age_months": 2,
            "dose_number": 1,
            "is_required": True
        },
        {
            "name": "PCV13",
            "description": "Pneumococcal conjugate vaccine",
            "recommended_age_months": 2,
            "dose_number": 1,
            "is_required": True
        },
        {
            "name": "Rotavirus",
            "description": "Protects against rotavirus infection",
            "recommended_age_months": 2,
            "dose_number": 1,
            "is_required": True
        },
        {
            "name": "MMR",
            "description": "Measles, Mumps, Rubella vaccine",
            "recommended_age_months": 12,
            "dose_number": 1,
            "is_required": True
        },
        {
            "name": "Varicella",
            "description": "Chickenpox vaccine",
            "recommended_age_months": 12,
            "dose_number": 1,
            "is_required": True
        },
        {
            "name": "Hepatitis A",
            "description": "Protects against hepatitis A virus infection",
            "recommended_age_months": 12,
            "dose_number": 1,
            "is_required": True
        },
        {
            "name": "Meningococcal",
            "description": "Protects against meningococcal disease",
            "recommended_age_months": 12,
            "dose_number": 1,
            "is_required": False
        }
    ]
    
    for vaccine_data in vaccines_data:
        # Check if vaccine already exists
        existing = Vaccine.find_by_name(vaccine_data["name"])
        if not existing:
            Vaccine.create(
                vaccine_data["name"],
                vaccine_data["description"],
                vaccine_data["recommended_age_months"],
                vaccine_data["dose_number"],
                vaccine_data["is_required"]
            )
    
    print(f"Seeded {len(vaccines_data)} vaccines")

def seed_sample_user():
    """Seed a sample user for testing"""
    print("Seeding sample user...")
    
    # Check if sample user already exists
    existing_user = User.find_by_username("demo_user")
    if existing_user:
        print("Sample user already exists")
        return existing_user
    
    user = User.create(
        username="demo_user",
        email="demo@example.com",
        password="password123",
        language="en"
    )
    
    print("Sample user created: demo_user / password123")
    return user

def seed_sample_child(user):
    """Seed a sample child for testing"""
    print("Seeding sample child...")
    
    # Check if sample child already exists
    existing_children = Child.find_by_user_id(user.id)
    if existing_children:
        print("Sample child already exists")
        return existing_children[0]
    
    # Create a child born 6 months ago
    birth_date = date.today() - timedelta(days=180)
    child = Child.create(
        user_id=user.id,
        name="Baby Emma",
        date_of_birth=birth_date,
        gender="female"
    )
    
    print("Sample child created: Baby Emma")
    return child

def seed_sample_schedules(child):
    """Seed sample vaccine schedules for the child"""
    print("Seeding sample vaccine schedules...")
    
    # Get vaccines appropriate for child's age
    age_months = child.age_in_months
    vaccines = Vaccine.find_by_age_months(age_months)
    
    schedules_created = 0
    for vaccine in vaccines:
        # Calculate scheduled date based on recommended age
        scheduled_date = child.date_of_birth + timedelta(days=vaccine.recommended_age_months * 30)
        
        # Only schedule if not already scheduled and date is in the future
        if scheduled_date >= date.today():
            child_vaccine = ChildVaccine.create(child.id, vaccine.id, scheduled_date)
            
            # Create reminder
            reminder_date = scheduled_date - timedelta(days=7)  # 1 week before
            if reminder_date >= date.today():
                message = f"Reminder: {child.name} is due for {vaccine.name} on {scheduled_date}"
                Reminder.create(child_vaccine.id, reminder_date, message)
            
            schedules_created += 1
    
    print(f"Created {schedules_created} vaccine schedules")

def seed_all():
    """Seed all data"""
    print("Starting database seeding...")
    print()
    
    try:
        seed_vaccines()
        print()
        
        user = seed_sample_user()
        print()
        
        child = seed_sample_child(user)
        print()
        
        seed_sample_schedules(child)
        print()
        
        print("Database seeding completed successfully!")
        print()
        print("Sample login credentials:")
        print("Username: demo_user")
        print("Password: password123")
        print()
        print("The sample child 'Baby Emma' has been created with")
        print("appropriate vaccine schedules based on her age.")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        conn, _ = get_db()
        conn.rollback()
        conn.close()

if __name__ == "__main__":
    seed_all()

