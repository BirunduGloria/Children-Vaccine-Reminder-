# lib/helpers.py
from models.user import User
from models.child import Child
from models.vaccine import Vaccine
from models.child_vaccine import ChildVaccine
from models.reminder import Reminder
from datetime import datetime, date, timedelta
import os

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    print("=" * 60)
    print("           CHILD VACCINE REMINDER APP")
    print("=" * 60)
    print()

def print_success(message):
    """Print success message"""
    print(f" {message}")

def print_error(message):
    """Print error message"""
    print(f" {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ {message}")

def print_warning(message):
    """Print warning message"""
    print(f"{message}")

def get_valid_date(prompt):
    """Get a valid date from user input"""
    while True:
        try:
            date_str = input(prompt + " (YYYY-MM-DD): ").strip()
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print_error("Invalid date format. Please use YYYY-MM-DD")

def get_valid_int(prompt, min_value=None, max_value=None):
    """Get a valid integer from user input"""
    while True:
        try:
            value = int(input(prompt + ": ").strip())
            if min_value is not None and value < min_value:
                print_error(f"Value must be at least {min_value}")
                continue
            if max_value is not None and value > max_value:
                print_error(f"Value must be at most {max_value}")
                continue
            return value
        except ValueError:
            print_error("Please enter a valid number")

def get_valid_choice(prompt, valid_choices):
    """Get a valid choice from user input"""
    while True:
        choice = input(prompt + ": ").strip().lower()
        if choice in valid_choices:
            return choice
        print_error(f"Please choose from: {', '.join(valid_choices)}")

def exit_program():
    """Exit the program"""
    print_header()
    print("Thank you for using the Children Vaccine Reminder App!")
    print("Stay healthy and keep your children protected! ")
    print()
    exit()

# User Management Functions
def register_user():
    """Register a new user"""
    print_header()
    print(" USER REGISTRATION")
    print("-" * 30)
    
    try:
        username = input("Username: ").strip()
        if User.find_by_username(username):
            print_error("Username already exists")
            return None
        
        email = input("Email: ").strip()
        if User.find_by_email(email):
            print_error("Email already registered")
            return None
        
        password = input("Password: ").strip()
        if len(password) < 6:
            print_error("Password must be at least 6 characters")
            return None
        
        language = get_valid_choice("Language (en/es/fr/de/ar/zh)", ['en', 'es', 'fr', 'de', 'ar', 'zh'])
        
        user = User.create(username, email, password, language)
        print_success(f"User {username} registered successfully!")
        return user
        
    except ValueError as e:
        print_error(str(e))
        return None

def login_user():
    """Login existing user"""
    print_header()
    print("USER LOGIN")
    print("-" * 30)
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    user = User.authenticate(username, password)
    if user:
        print_success(f"Welcome back, {user.username}!")
        return user
    else:
        print_error("Invalid username or password")
        return None

# Child Management Functions
def add_child_profile(user):
    """Add a new child profile"""
    print_header()
    print(" ADD CHILD PROFILE")
    print("-" * 30)
    
    try:
        name = input("Child's name: ").strip()
        if len(name) < 2:
            print_error("Name must be at least 2 characters")
            return None
        
        date_of_birth = get_valid_date("Date of birth")
        if date_of_birth > date.today():
            print_error("Date of birth cannot be in the future")
            return None
        
        gender = get_valid_choice("Gender (male/female/other)", ['male', 'female', 'other'])
        
        child = Child.create(user.id, name, date_of_birth, gender)
        print_success(f"Child profile for {name} created successfully!")
        
        # Auto-schedule vaccines based on age
        schedule_vaccines_for_child(child)
        
        return child
        
    except ValueError as e:
        print_error(str(e))
        return None

def schedule_vaccines_for_child(child):
    """Automatically schedule vaccines for a child based on their age"""
    age_months = child.age_in_months
    
    # Get vaccines appropriate for child's age
    vaccines = Vaccine.find_by_age_months(age_months)
    
    for vaccine in vaccines:
        # Calculate scheduled date based on recommended age
        scheduled_date = child.date_of_birth + timedelta(days=vaccine.recommended_age_months * 30)
        
        # Only schedule if not already scheduled
        existing = ChildVaccine.find_by_child_id(child.id)
        vaccine_ids = [cv.vaccine_id for cv in existing]
        
        if vaccine.id not in vaccine_ids:
            child_vaccine = ChildVaccine.create(child.id, vaccine.id, scheduled_date)
            
            # Create reminder
            reminder_date = scheduled_date - timedelta(days=7)  # 1 week before
            if reminder_date >= date.today():
                message = f"Reminder: {child.name} is due for {vaccine.name} on {scheduled_date}"
                Reminder.create(child_vaccine.id, reminder_date, message)

def view_child_profiles(user):
    """View all child profiles for a user"""
    print_header()
    print(" CHILD PROFILES")
    print("-" * 30)
    
    children = Child.find_by_user_id(user.id)
    
    if not children:
        print_info("No children profiles found. Add a child profile first.")
        return
    
    for i, child in enumerate(children, 1):
        print(f"{i}. {child.name}")
        print(f"   Date of Birth: {child.date_of_birth}")
        print(f"   Age: {child.age_in_months} months ({child.age_in_years} years)")
        print(f"   Gender: {child.gender.capitalize()}")
        print()

def delete_child_profile(user):
    """Delete a child profile"""
    print_header()
    print(" DELETE CHILD PROFILE")
    print("-" * 30)
    
    children = Child.find_by_user_id(user.id)
    
    if not children:
        print_info("No children profiles found.")
        return
    
    print("Select child to delete:")
    for i, child in enumerate(children, 1):
        print(f"{i}. {child.name}")
    
    try:
        choice = get_valid_int("Enter choice", 1, len(children))
        child = children[choice - 1]
        
        confirm = input(f"Are you sure you want to delete {child.name}'s profile? (yes/no): ").strip().lower()
        if confirm == 'yes':
            child.delete()
            print_success(f"{child.name}'s profile deleted successfully!")
        else:
            print_info("Deletion cancelled.")
            
    except ValueError as e:
        print_error(str(e))

# Vaccine Management Functions
def view_vaccine_schedule(child):
    """View vaccine schedule for a specific child"""
    print_header()
    print(f" VACCINE SCHEDULE FOR {child.name.upper()}")
    print("-" * 50)
    
    child_vaccines = ChildVaccine.find_by_child_id(child.id)
    
    if not child_vaccines:
        print_info("No vaccines scheduled for this child.")
        return
    
    print(f"Age: {child.age_in_months} months ({child.age_in_years} years)")
    print()
    
    # Group by status
    scheduled = [cv for cv in child_vaccines if cv.status == 'scheduled']
    completed = [cv for cv in child_vaccines if cv.status == 'completed']
    overdue = [cv for cv in child_vaccines if cv.status == 'overdue']
    
    if overdue:
        print(" OVERDUE VACCINES:")
        for cv in overdue:
            vaccine = cv.get_vaccine()
            days_overdue = abs(cv.days_until_due)
            print(f"   • {vaccine.name} - Due: {cv.scheduled_date} ({days_overdue} days overdue)")
        print()
    
    if scheduled:
        print(" UPCOMING VACCINES:")
        for cv in scheduled:
            vaccine = cv.get_vaccine()
            if cv.is_due_soon:
                print(f"   • {vaccine.name} - Due: {cv.scheduled_date} (Due soon!)")
            else:
                print(f"   • {vaccine.name} - Due: {cv.scheduled_date} (in {cv.days_until_due} days)")
        print()
    
    if completed:
        print(" COMPLETED VACCINES:")
        for cv in completed:
            vaccine = cv.get_vaccine()
            print(f"   • {vaccine.name} - Completed: {cv.completed_date}")
        print()

def mark_vaccine_complete(child):
    """Mark a vaccine as complete"""
    print_header()
    print(f"MARK VACCINE COMPLETE FOR {child.name.upper()}")
    print("-" * 50)
    
    # Get vaccines that are not completed
    child_vaccines = [cv for cv in ChildVaccine.find_by_child_id(child.id) if cv.status != 'completed']
    
    if not child_vaccines:
        print_info("All vaccines are already completed!")
        return
    
    print("Select vaccine to mark as complete:")
    for i, cv in enumerate(child_vaccines, 1):
        vaccine = cv.get_vaccine()
        status = "OVERDUE" if cv.status == 'overdue' else "SCHEDULED"
        print(f"{i}. {vaccine.name} - {status} - Due: {cv.scheduled_date}")
    
    try:
        choice = get_valid_int("Enter choice", 1, len(child_vaccines))
        child_vaccine = child_vaccines[choice - 1]
        
        completed_date = get_valid_date("Completion date")
        child_vaccine.mark_completed(completed_date)
        
        vaccine = child_vaccine.get_vaccine()
        print_success(f"{vaccine.name} marked as complete!")
        
    except ValueError as e:
        print_error(str(e))

def view_all_vaccines():
    """View all available vaccines"""
    print_header()
    print(" AVAILABLE VACCINES")
    print("-" * 30)
    
    vaccines = Vaccine.get_all()
    
    if not vaccines:
        print_info("No vaccines found in the system.")
        return
    
    for vaccine in vaccines:
        required = "Required" if vaccine.is_required else "Optional"
        print(f"• {vaccine.name}")
        print(f"  Description: {vaccine.description}")
        print(f"  Recommended Age: {vaccine.recommended_age_months} months")
        print(f"  Dose: {vaccine.dose_number}")
        print(f"  Status: {required}")
        print()

# Reminder Functions
def view_reminders(user):
    """View all reminders for a user's children"""
    print_header()
    print(" VACCINE REMINDERS")
    print("-" * 30)
    
    children = Child.find_by_user_id(user.id)
    
    if not children:
        print_info("No children profiles found.")
        return
    
    all_reminders = []
    for child in children:
        child_vaccines = ChildVaccine.find_by_child_id(child.id)
        for cv in child_vaccines:
            reminders = Reminder.find_by_child_vaccine_id(cv.id)
            all_reminders.extend(reminders)
    
    if not all_reminders:
        print_info("No reminders found.")
        return
    
    # Sort by reminder date
    all_reminders.sort(key=lambda r: r.reminder_date)
    
    print("Upcoming Reminders:")
    for reminder in all_reminders:
        child_vaccine = reminder.get_child_vaccine()
        child = child_vaccine.get_child()
        vaccine = child_vaccine.get_vaccine()
        
        status = "SENT" if reminder.sent else "PENDING"
        print(f"• {child.name} - {vaccine.name}")
        print(f"  Reminder Date: {reminder.reminder_date}")
        print(f"  Status: {status}")
        print(f"  Message: {reminder.message}")
        print()

def check_overdue_vaccines(user):
    """Check for overdue vaccines across all children"""
    print_header()
    print("OVERDUE VACCINES CHECK")
    print("-" * 30)
    
    children = Child.find_by_user_id(user.id)
    
    if not children:
        print_info("No children profiles found.")
        return
    
    overdue_found = False
    for child in children:
        overdue_vaccines = ChildVaccine.find_overdue_by_child_id(child.id)
        
        if overdue_vaccines:
            overdue_found = True
            print(f" {child.name} has {len(overdue_vaccines)} overdue vaccine(s):")
            
            for cv in overdue_vaccines:
                vaccine = cv.get_vaccine()
                days_overdue = abs(cv.days_until_due)
                print(f"   • {vaccine.name} - {days_overdue} days overdue")
            print()
    
    if not overdue_found:
        print_success("No overdue vaccines found! All children are up to date.")

def exit_program():
    """Exit the program"""
    print_header()
    print("Thank you for using the Children Vaccine Reminder App!")
    print("Stay healthy and keep your children protected! ")
    print()
    exit()
