from .helpers import (
    clear_screen, print_header, print_success, print_error, print_info,
    register_user, login_user, add_child_profile, view_child_profiles,
    delete_child_profile, view_vaccine_schedule, mark_vaccine_complete,
    view_all_vaccines, view_reminders, check_overdue_vaccines, exit_program
)
from .models.user import User
from .models.child import Child
from .models.vaccine import Vaccine
from .models.child_vaccine import ChildVaccine
from .models.reminder import Reminder
from datetime import datetime, date, timedelta
import os

def main():
    """Main application loop"""
    current_user = None
    
    while True:
        if current_user is None:
            current_user = show_login_menu()
        else:
            show_main_menu(current_user)
            choice = input("> ")
            
            if choice == "0":
                current_user = None  # Logout
                clear_screen()
                print_success("Logged out successfully!")
            elif choice == "1":
                manage_child_profiles(current_user)
            elif choice == "2":
                manage_vaccines(current_user)
            elif choice == "3":
                manage_reminders(current_user)
            elif choice == "4":
                set_next_vaccine_reminder(current_user)
            elif choice == "5":
                view_health_records(current_user)
            elif choice == "6":
                manage_account(current_user)
            elif choice == "7":
                exit_program()
            else:
                print_error("Invalid choice. Please try again.")

def show_login_menu():
    """Show login/registration menu"""
    while True:
        print_header()
        print("WELCOME TO VACCINE REMINDER APP")
        print("-" * 40)
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        print()
        
        choice = input("> ")
        
        if choice == "1":
            user = login_user()
            if user:
                return user
        elif choice == "2":
            user = register_user()
            if user:
                return user
        elif choice == "0":
            exit_program()
        else:
            print_error("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

def show_main_menu(user):
    """Show main application menu"""
    print_header()
    print(f" Welcome, {user.username}!")
    print(f"Language: {user.language.upper()}")
    print("-" * 40)
    print("1. Manage Child Profiles")
    print("2. Manage Vaccines")
    print("3. Manage Reminders")
    print("4. Set Next Vaccine Reminder")
    print("5. View Health Records")
    print("6. Account Settings")
    print("0. Logout")
    print("7. Exit Program")
    print()

def manage_child_profiles(user):
    """Manage child profiles submenu"""
    while True:
        print_header()
        print("CHILD PROFILE MANAGEMENT")
        print("-" * 40)
        print("1. Add New Child Profile")
        print("2. View Child Profiles")
        print("3. Delete Child Profile")
        print("4. View Vaccine Schedule")
        print("5. Mark Vaccine Complete")
        print("6. Schedule Vaccine for Child")
        print("0. Back to Main Menu")
        print()
        
        choice = input("> ")
        
        if choice == "1":
            add_child_profile(user)
            input("\nPress Enter to continue...")
        elif choice == "2":
            view_child_profiles(user)
            input("\nPress Enter to continue...")
        elif choice == "3":
            delete_child_profile(user)
            input("\nPress Enter to continue...")
        elif choice == "4":
            select_child_for_schedule(user)
            input("\nPress Enter to continue...")
        elif choice == "5":
            select_child_for_completion(user)
            input("\nPress Enter to continue...")
        elif choice == "6":
            schedule_vaccine_for_child(user)
            input("\nPress Enter to continue...")
        elif choice == "0":
            break
        else:
            print_error("Invalid choice. Please try again.")

def manage_vaccines(user):
    """Manage vaccines submenu"""
    while True:
        print_header()
        print("VACCINE MANAGEMENT")
        print("-" * 40)
        print("1. View All Available Vaccines")
        print("2. Check Overdue Vaccines")
        print("3. View Due Soon Vaccines")
        print("0. Back to Main Menu")
        print()
        
        choice = input("> ")
        
        if choice == "1":
            view_all_vaccines()
            input("\nPress Enter to continue...")
        elif choice == "2":
            check_overdue_vaccines(user)
            input("\nPress Enter to continue...")
        elif choice == "3":
            view_due_soon_vaccines(user)
            input("\nPress Enter to continue...")
        elif choice == "0":
            break
        else:
            print_error("Invalid choice. Please try again.")

def manage_reminders(user):
    """Manage reminders submenu"""
    while True:
        print_header()
        print("REMINDER MANAGEMENT")
        print("-" * 40)
        print("1. View All Reminders")
        print("2. View Due Reminders")
        print("3. Create Custom Reminder")
        print("0. Back to Main Menu")
        print()
        
        choice = input("> ")
        
        if choice == "1":
            view_reminders(user)
            input("\nPress Enter to continue...")
        elif choice == "2":
            view_due_reminders(user)
            input("\nPress Enter to continue...")
        elif choice == "3":
            create_custom_reminder(user)
            input("\nPress Enter to continue...")
        elif choice == "0":
            break
        else:
            print_error("Invalid choice. Please try again.")

def view_health_records(user):
    """View comprehensive health records"""
    print_header()
    print(" HEALTH RECORDS OVERVIEW")
    print("-" * 40)
    
    children = Child.find_by_user_id(user.id)
    
    if not children:
        print_info("No children profiles found. Add a child profile first.")
        return
    
    for child in children:
        print(f" {child.name.upper()}")
        print(f"   Date of Birth: {child.date_of_birth}")
        print(f"   Age: {child.age_in_months} months ({child.age_in_years} years)")
        print(f"   Gender: {child.gender.capitalize()}")
        
        # Vaccine summary
        child_vaccines = ChildVaccine.find_by_child_id(child.id)
        total_vaccines = len(child_vaccines)
        completed_vaccines = len([cv for cv in child_vaccines if cv.status == 'completed'])
        overdue_vaccines = len([cv for cv in child_vaccines if cv.status == 'overdue'])
        
        print(f"   Vaccines: {completed_vaccines}/{total_vaccines} completed")
        if overdue_vaccines > 0:
            print(f"     {overdue_vaccines} overdue vaccines")
        
        print()
    
    input("\nPress Enter to continue...")

def manage_account(user):
    """Manage account settings"""
    while True:
        print_header()
        print(" ACCOUNT SETTINGS")
        print("-" * 40)
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Language: {user.language.upper()}")
        print(f"Member since: {user.created_at.strftime('%Y-%m-%d')}")
        print()
        print("1. Change Language")
        print("2. Change Password")
        print("3. Delete Account")
        print("0. Back to Main Menu")
        print()
        
        choice = input("> ")
        
        if choice == "1":
            change_language(user)
        elif choice == "2":
            change_password(user)
        elif choice == "3":
            if delete_account(user):
                return None  # Logout user
        elif choice == "0":
            break
        else:
            print_error("Invalid choice. Please try again.")

def select_child_for_schedule(user):
    """Select a child to view vaccine schedule"""
    children = Child.find_by_user_id(user.id)
    
    if not children:
        print_info("No children profiles found. Add a child profile first.")
        return
    
    print("Select child to view vaccine schedule:")
    for i, child in enumerate(children, 1):
        print(f"{i}. {child.name}")
    
    try:
        choice = int(input("Enter choice: ").strip())
        if 1 <= choice <= len(children):
            child = children[choice - 1]
            view_vaccine_schedule(child)
        else:
            print_error("Invalid choice.")
    except ValueError:
        print_error("Please enter a valid number.")

def select_child_for_completion(user):
    """Select a child to mark vaccine complete"""
    children = Child.find_by_user_id(user.id)
    
    if not children:
        print_info("No children profiles found. Add a child profile first.")
        return
    
    print("Select child to mark vaccine complete:")
    for i, child in enumerate(children, 1):
        print(f"{i}. {child.name}")
    
    try:
        choice = int(input("Enter choice: ").strip())
        if 1 <= choice <= len(children):
            child = children[choice - 1]
            mark_vaccine_complete(child)
        else:
            print_error("Invalid choice.")
    except ValueError:
        print_error("Please enter a valid number.")

def schedule_vaccine_for_child(user):
    """Allow user to schedule a vaccine for a selected child and show educational info."""
    children = Child.find_by_user_id(user.id)
    if not children:
        print_info("No children profiles found. Add a child profile first.")
        return
    print("Select child to schedule a vaccine:")
    for i, child in enumerate(children, 1):
        print(f"{i}. {child.name}")
    try:
        choice = int(input("Enter choice: ").strip())
    except ValueError:
        print_error("Please enter a valid number.")
        return
    if not (1 <= choice <= len(children)):
        print_error("Invalid choice.")
        return
    child = children[choice - 1]
    # List all vaccines
    vaccines = Vaccine.get_all()
    print(f"Available vaccines to schedule for {child.name}:")
    for i, vaccine in enumerate(vaccines, 1):
        print(f"{i}. {vaccine.name} (Recommended at {vaccine.recommended_age_months} months)")
    try:
        vchoice = int(input("Select vaccine: ").strip())
    except ValueError:
        print_error("Please enter a valid number.")
        return
    if not (1 <= vchoice <= len(vaccines)):
        print_error("Invalid choice.")
        return
    vaccine = vaccines[vchoice - 1]
    scheduled_date = input("Enter scheduled date (YYYY-MM-DD): ").strip()
    try:
        ChildVaccine.create(child.id, vaccine.id, scheduled_date)
        print_success(f"Vaccine {vaccine.name} scheduled for {child.name} on {scheduled_date}.")
        # Show educational insights
        print("\nEducational Insights:")
        print(f"Vaccine: {vaccine.name}")
        print(f"Description: {vaccine.description}")
        print(f"Recommended Age: {vaccine.recommended_age_months} months")
        print(f"Dose Number: {vaccine.dose_number}")
        print(f"Required: {'Yes' if vaccine.is_required else 'No'}")
        notify_email_reminder_policy()
    except Exception as e:
        print_error(f"Failed to schedule vaccine: {e}")

def view_due_soon_vaccines(user):
    """View vaccines due soon for all children"""
    print_header()
    print("VACCINES DUE SOON (Next 7 days)")
    print("-" * 50)
    
    children = Child.find_by_user_id(user.id)
    
    if not children:
        print_info("No children profiles found.")
        return
    
    due_soon_found = False
    for child in children:
        upcoming_vaccines = ChildVaccine.find_upcoming_by_child_id(child.id)
        due_soon = [cv for cv in upcoming_vaccines if cv.is_due_soon]
        
        if due_soon:
            due_soon_found = True
            print(f" {child.name}:")
            for cv in due_soon:
                vaccine = cv.get_vaccine()
                print(f"   • {vaccine.name} - Due: {cv.scheduled_date} (in {cv.days_until_due} days)")
            print()
    
    if not due_soon_found:
        print_success("No vaccines due in the next 7 days!")

def view_due_reminders(user):
    """View reminders that are due"""
    print_header()
    print(" DUE REMINDERS")
    print("-" * 30)
    
    due_reminders = Reminder.find_due_reminders()
    
    if not due_reminders:
        print_info("No due reminders found.")
        return
    
    for reminder in due_reminders:
        child_vaccine = reminder.get_child_vaccine()
        child = child_vaccine.get_child()
        vaccine = child_vaccine.get_vaccine()
        
        print(f"• {child.name} - {vaccine.name}")
        print(f"  Due: {reminder.reminder_date}")
        print(f"  Message: {reminder.message}")
        print()

def create_custom_reminder(user):
    """Create a custom reminder for a child's vaccine"""
    print_header()
    print(" CREATE CUSTOM REMINDER")
    print("-" * 30)
    
    children = Child.find_by_user_id(user.id)
    
    if not children:
        print_info("No children profiles found. Add a child profile first.")
        return
    
    print("Select child:")
    for i, child in enumerate(children, 1):
        print(f"{i}. {child.name}")
    
    try:
        choice = int(input("Enter choice: ").strip())
        if 1 <= choice <= len(children):
            child = children[choice - 1]
            create_reminder_for_child(child)
        else:
            print_error("Invalid choice.")
    except ValueError:
        print_error("Please enter a valid number.")

def create_reminder_for_child(child):
    """Create a reminder for a specific child"""
    child_vaccines = ChildVaccine.find_by_child_id(child.id)
    
    if not child_vaccines:
        print_info("No vaccines scheduled for this child.")
        return
    
    print(f"\nSelect vaccine for {child.name}:")
    for i, cv in enumerate(child_vaccines, 1):
        vaccine = cv.get_vaccine()
        print(f"{i}. {vaccine.name} - Due: {cv.scheduled_date}")
    
    try:
        choice = int(input("Enter choice: ").strip())
        if 1 <= choice <= len(child_vaccines):
            child_vaccine = child_vaccines[choice - 1]
            
            reminder_date = input("Reminder date (YYYY-MM-DD): ").strip()
            message = input("Reminder message: ").strip()
            
            if reminder_date and message:
                reminder = Reminder.create(child_vaccine.id, reminder_date, message)
                print_success("Custom reminder created successfully!")
            else:
                print_error("Reminder date and message are required.")
        else:
            print_error("Invalid choice.")
    except ValueError as e:
        print_error(str(e))

def change_language(user):
    """Change user's preferred language"""
    print_header()
    print(" CHANGE LANGUAGE")
    print("-" * 30)
    
    languages = ['en', 'swahili']
    language_names = {
        'en': 'English', 
        'sw' : 'Swahili'
    
    }
    
    
    print("Available languages:")
    for i, lang in enumerate(languages, 1):
        print(f"{i}. {language_names[lang]}")
    
    try:
        choice = int(input("Enter choice: ").strip())
        if 1 <= choice <= len(languages):
            new_language = languages[choice - 1]
            user.language = new_language
            user.save()
            print_success(f"Language changed to {language_names[new_language]}!")
        else:
            print_error("Invalid choice.")
    except ValueError:
        print_error("Please enter a valid number.")
    
    input("\nPress Enter to continue...")

def change_password(user):
    """Change user's password"""
    print_header()
    print(" CHANGE PASSWORD")
    print("-" * 30)
    
    current_password = input("Current password: ").strip()
    
    # Verify current password
    if not User.authenticate(user.username, current_password):
        print_error("Current password is incorrect.")
        input("\nPress Enter to continue...")
        return
    
    new_password = input("New password: ").strip()
    confirm_password = input("Confirm new password: ").strip()
    
    if new_password != confirm_password:
        print_error("Passwords do not match.")
    elif len(new_password) < 6:
        print_error("Password must be at least 6 characters long.")
    else:
        # Hash and save new password
        import hashlib
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        user.password_hash = new_password_hash
        user.save()
        print_success("Password changed successfully!")
    
    input("\nPress Enter to continue...")

def delete_account(user):
    """Delete user account"""
    print_header()
    print("  DELETE ACCOUNT")
    print("-" * 30)
    
    print(" WARNING: This action cannot be undone!")
    print(f"All data for user '{user.username}' will be permanently deleted.")
    print("This includes:")
    print("  - Child profiles")
    print("  - Vaccine schedules")
    print("  - Reminders")
    print("  - Health records")
    print()
    
    confirm = input("Are you absolutely sure? Type 'DELETE' to confirm: ").strip()
    
    if confirm == "DELETE":
        # Delete all related data first
        children = Child.find_by_user_id(user.id)
        for child in children:
            child_vaccines = ChildVaccine.find_by_child_id(child.id)
            for cv in child_vaccines:
                reminders = Reminder.find_by_child_vaccine_id(cv.id)
                for reminder in reminders:
                    reminder.delete()
                cv.delete()
            child.delete()
        
        # Delete user
        user.delete()
        print_success("Account deleted successfully!")
        return True
    else:
        print_info("Account deletion cancelled.")
        return False

def set_next_vaccine_reminder(user):
    """Streamlined flow: select child, show next vaccine, set reminder, then log out."""
    children = Child.find_by_user_id(user.id)
    if not children:
        print_info("No children profiles found. Add a child profile first.")
        return
    print("Select child to set next vaccine reminder:")
    for i, child in enumerate(children, 1):
        print(f"{i}. {child.name}")
    try:
        choice = int(input("Enter choice: ").strip())
    except ValueError:
        print_error("Please enter a valid number.")
        return
    if not (1 <= choice <= len(children)):
        print_error("Invalid choice.")
        return
    child = children[choice - 1]
    # List all upcoming vaccines for the child
    upcoming = [cv for cv in ChildVaccine.find_by_child_id(child.id) if cv.status == 'scheduled' and cv.scheduled_date >= date.today()]
    if not upcoming:
        print_info("No upcoming vaccines for this child.")
        return
    print(f"Upcoming vaccines for {child.name}:")
    for i, cv in enumerate(upcoming, 1):
        vaccine = cv.get_vaccine()
        print(f"{i}. {vaccine.name} - Due: {cv.scheduled_date}")
    try:
        vchoice = int(input("Select vaccine to set reminder for: ").strip())
    except ValueError:
        print_error("Please enter a valid number.")
        return
    if not (1 <= vchoice <= len(upcoming)):
        print_error("Invalid choice.")
        return
    selected_cv = upcoming[vchoice - 1]
    vaccine = selected_cv.get_vaccine()
    print(f"Setting reminder for {vaccine.name} on {selected_cv.scheduled_date}")
    reminder_date = input("Reminder date (YYYY-MM-DD): ").strip()
    message = input("Reminder message: ").strip()
    if reminder_date and message:
        Reminder.create(selected_cv.id, reminder_date, message)
        print_success("Reminder set successfully!")
        print_success("Logging out...")
        exit_program()
    else:
        print_error("Reminder date and message are required.")
        return

def view_vaccine_schedule(child):
    """Display the vaccine schedule for a child in a table format."""
    from .models.child_vaccine import ChildVaccine
    print(f"\nVaccine Schedule for {child.name}:")
    print("-" * 70)
    print(f"{'Vaccine':20} | {'Scheduled Date':15} | {'Status':10} | {'Completed Date':15}")
    print("-" * 70)
    child_vaccines = ChildVaccine.find_by_child_id(child.id)
    if not child_vaccines:
        print_info("No vaccines scheduled for this child.")
        return
    for cv in child_vaccines:
        vaccine = cv.get_vaccine()
        completed = cv.completed_date if cv.completed_date else "-"
        print(f"{vaccine.name:20} | {str(cv.scheduled_date):15} | {cv.status:10} | {str(completed):15}")
    print("-" * 70)

def notify_email_reminder_policy():
    print("\nNOTE: Email reminders are mandatory for all users.")
    print("You will receive an email 3 days before each scheduled vaccine date.\n")

def register_user_with_notification():
    user = register_user()
    if user:
        notify_email_reminder_policy()
    return user

if __name__ == "__main__":
    main()
