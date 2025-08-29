from ..db import get_db
import hashlib
from datetime import datetime

# User model handles user registration, authentication, and user data
class User:
    @classmethod
    def authenticate(cls, username, password):
        import hashlib
        user = cls.find_by_username(username)
        if not user:
            return None
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash == password_hash:
            return user
        return None
    def __init__(self, username, email, password_hash, language="en", id=None, created_at=None):
        # User attributes
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.language = language
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        # String representation for debugging and display
        return f"<User {self.username} ({self.email})>"

    # Property methods for validation and encapsulation
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        # Username must be at least 3 characters
        if not value or len(value.strip()) < 3:
            raise ValueError("Username must be at least 3 characters long")
        self._username = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # Email must be valid format
        def save(self):
            # Save or update user in the database
            conn, cursor = get_db()
            if self.id:
                cursor.execute("""
                    UPDATE users SET username=?, email=?, password_hash=?, language=? WHERE id=?
                """, (self.username, self.email, self.password_hash, self.language, self.id))
            else:
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, language, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.username, self.email, self.password_hash, self.language, self.created_at))
                self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            return self
        if not value or '@' not in value:
            raise ValueError("Email must be a valid email address")
        self._email = value.lower().strip()

    @property
    def password_hash(self):
        return self._password_hash
    @password_hash.setter
    def password_hash(self, value):
        # Password must be at least 6 characters
        if not value or len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self._password_hash = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        # Only allow supported languages
        valid_languages = ['en']
        if value not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(valid_languages)}")
        self._language = value

    # ORM Methods for database interaction
    def save(self):
        # Save or update user in the database
        conn, cursor = get_db()
        if self.id:
            cursor.execute("""
                UPDATE users SET username=?, email=?, password_hash=?, language=? WHERE id=?
            """, (self.username, self.email, self.password_hash, self.language, self.id))
        else:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, language, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (self.username, self.email, self.password_hash, self.language, self.created_at))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    def delete(self):
        if self.id:
            conn, cursor = get_db()
            cursor.execute("DELETE FROM users WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()
            self.id = None
            return True
        return False

    @classmethod
    def create(cls, username, email, password, language="en"):
        # Hash the password before saving
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = cls(username, email, password_hash, language)
        user.save()
        return user

    @classmethod
    def find_by_username(cls, username):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[0], row[5])
        return None

    @classmethod
    def find_by_email(cls, email):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[0], row[5])
        return None

    @classmethod
    def find_by_id(cls, id):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[0], row[5])
        return None

