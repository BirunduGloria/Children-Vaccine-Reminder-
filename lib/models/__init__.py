import sqlite3

CONN = sqlite3.connect('vaccine_reminder.db')
CURSOR = CONN.cursor()

# Create tables if they don't exist
def create_tables():
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            gender TEXT CHECK(gender IN ('male', 'female', 'other')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS vaccines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            recommended_age_months INTEGER NOT NULL,
            dose_number INTEGER DEFAULT 1,
            is_required BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS child_vaccines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            vaccine_id INTEGER NOT NULL,
            scheduled_date DATE NOT NULL,
            completed_date DATE,
            status TEXT DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'completed', 'overdue')),
            reminder_sent BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (child_id) REFERENCES children (id),
            FOREIGN KEY (vaccine_id) REFERENCES vaccines (id)
        )
    """)
    
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_vaccine_id INTEGER NOT NULL,
            reminder_date DATE NOT NULL,
            message TEXT NOT NULL,
            sent BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (child_vaccine_id) REFERENCES child_vaccines (id)
        )
    """)
    
    CONN.commit()

# Initialize tables
create_tables()

# Import all models
from .user import User
from .child import Child
from .vaccine import Vaccine
from .child_vaccine import ChildVaccine
from .reminder import Reminder

__all__ = ['User', 'Child', 'Vaccine', 'ChildVaccine', 'Reminder']
