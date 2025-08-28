# Children Vaccine Reminder App

A comprehensive Python CLI application that helps parents and caregivers manage their children's vaccine schedules, receive automated reminders, and maintain health records.

## 🌟 Features

### Core Functionality
- **User Management**: Secure registration and login system with multi-language support
- **Child Profiles**: Add and manage multiple children with birth date and gender information
- **Vaccine Scheduling**: Automatic vaccine scheduling based on child's age and standard recommendations
- **Smart Reminders**: Automated reminders for upcoming vaccines with customizable messages
- **Health Records**: Comprehensive tracking of completed, scheduled, and overdue vaccines
- **Multi-language Support**: Available in English, Spanish, French, German, Arabic, and Chinese

### Vaccine Management
- **Standard Vaccines**: Pre-loaded with CDC-recommended vaccine schedule
- **Age-based Scheduling**: Automatically calculates appropriate vaccine dates based on child's age
- **Status Tracking**: Monitor vaccines as scheduled, completed, or overdue
- **Educational Information**: Detailed descriptions and information about each vaccine

### Reminder System
- **Automated Reminders**: 7-day advance notifications for upcoming vaccines
- **Custom Reminders**: Create personalized reminders for specific needs
- **Overdue Alerts**: Track and manage overdue vaccines
- **Due Soon Notifications**: Identify vaccines due in the next 7 days

##  Architecture

### Object-Relational Mapping (ORM)
The application implements a custom ORM system with the following model classes:

- **User**: Manages user accounts with authentication and preferences
- **Child**: Represents children with age calculations and profile information
- **Vaccine**: Contains standard vaccine information and recommendations
- **ChildVaccine**: Manages the relationship between children and vaccines (one-to-many)
- **Reminder**: Handles vaccine reminders and notifications

### Database Design
- **SQLite Database**: Lightweight, file-based database for easy deployment
- **Relational Structure**: Proper foreign key relationships between tables
- **Data Integrity**: Constraints and validation at the database level

### CLI Interface
- **Menu-driven Navigation**: Intuitive command-line interface with clear options
- **Input Validation**: Comprehensive error handling and user input validation
- **User Experience**: Clear feedback, success messages, and error handling

## Getting Started

### Prerequisites
- Python 3.8.13 or higher
- pipenv for dependency management

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Children-Vaccine-Reminder-
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Seed the database with initial data**
   ```bash
   python lib/seed_data.py
   ```

4. **Run the application**
   ```bash
   python lib/cli.py
   ```

### Sample Login
After seeding the database, you can use these credentials:
- **Username**: demo_user
- **Password**: password123

## 📱 Usage

### Main Menu Options
1. **Manage Child Profiles**: Add, view, and delete child profiles
2. **Manage Vaccines**: View vaccine schedules and mark completions
3. **Manage Reminders**: View and create custom reminders
4. **View Health Records**: Comprehensive overview of all children's vaccine status
5. **Account Settings**: Change language, password, or delete account

### Adding a Child Profile
1. Select "Manage Child Profiles" from the main menu
2. Choose "Add New Child Profile"
3. Enter child's name, date of birth, and gender
4. The system automatically schedules appropriate vaccines

### Viewing Vaccine Schedule
1. Select "Manage Child Profiles" from the main menu
2. Choose "View Vaccine Schedule"
3. Select the child to view their complete vaccine timeline
4. See scheduled, completed, and overdue vaccines

### Marking Vaccines Complete
1. Select "Manage Child Profiles" from the main menu
2. Choose "Mark Vaccine Complete"
3. Select the child and vaccine to mark as complete
4. Enter the completion date

## 🗄️ Database Schema

### Tables
- **users**: User accounts and preferences
- **children**: Child profiles and information
- **vaccines**: Standard vaccine information
- **child_vaccines**: Vaccine scheduling and completion tracking
- **reminders**: Reminder system and notifications

### Relationships
- **User → Child**: One-to-many (one user can have multiple children)
- **Child → ChildVaccine**: One-to-many (one child can have multiple vaccine schedules)
- **Vaccine → ChildVaccine**: One-to-many (one vaccine can be scheduled for multiple children)
- **ChildVaccine → Reminder**: One-to-many (one vaccine schedule can have multiple reminders)

##  Technical Details

### ORM Methods
Each model class implements standard ORM methods:
- `create()`: Create new instances
- `save()`: Save changes to database
- `delete()`: Remove instances
- `find_by_id()`: Find by primary key
- `get_all()`: Retrieve all instances
- Custom finder methods for specific queries

### Property Validation
- Input validation using Python properties
- Constraint checking for data integrity
- Meaningful error messages for user feedback

### Error Handling
- Comprehensive exception handling
- User-friendly error messages
- Graceful degradation for invalid input

##  Multi-language Support
The application supports multiple languages:
- English (en) - Default
- Spanish (es)
- French (fr)
- German (de)
- Arabic (ar)
- Chinese (zh)

Users can change their preferred language through account settings.

##  Testing
The application includes comprehensive testing capabilities:
- Input validation testing
- Database operation testing
- Error handling verification
- User interaction testing

Run the application and test various scenarios:
- Invalid input handling
- Database operations
- User authentication
- Vaccine scheduling
- Reminder creation

##  Project Structure
```
lib/
├── models/
│   ├── __init__.py          # Database configuration and model imports
│   ├── user.py              # User model and authentication
│   ├── child.py             # Child profile management
│   ├── vaccine.py           # Vaccine information and scheduling
│   ├── child_vaccine.py     # Child-vaccine relationship management
│   └── reminder.py          # Reminder system
├── cli.py                   # Main CLI interface
├── helpers.py               # Helper functions and business logic
├── seed_data.py             # Database seeding and sample data
└── debug.py                 # Debug utilities
```

## Contributing
This project follows best practices for:
- Object-Oriented Programming
- Database design and ORM implementation
- CLI design and user experience
- Code organization and modularity
- Error handling and validation

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

##  Support
For questions or issues:
1. Check the error messages for guidance
2. Verify input format (especially dates: YYYY-MM-DD)
3. Ensure the database is properly seeded
4. Check Python version compatibility

##  Learning Goals Achieved
This project demonstrates:
- ✅ Python CLI application development
- ✅ Object-Relational Mapping implementation
- ✅ One-to-many relationships between classes
- ✅ CLI best practices and user experience
- ✅ OOP best practices and design patterns
- ✅ Database design and management
- ✅ Input validation and error handling
- ✅ Modular code organization

---

**Stay healthy and keep your children protected! **
