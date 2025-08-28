from models import CONN, CURSOR
import hashlib
from datetime import datetime

class User:
    def __init__(self, username, email, password_hash, language="en", id=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.language = language
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("Username must be at least 3 characters long")
        self._username = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or '@' not in value:
            raise ValueError("Email must be a valid email address")
        self._email = value.lower().strip()

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, value):
        if not value or len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self._password_hash = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        valid_languages = ['en', 'es', 'fr', 'de', 'ar', 'zh']
        if value not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(valid_languages)}")
        self._language = value

    # ORM Methods
    def save(self):
        if self.id:
            CURSOR.execute("""
                UPDATE users 
                SET username = ?, email = ?, password_hash = ?, language = ?
                WHERE id = ?
            """, (self.username, self.email, self.password_hash, self.language, self.id))
        else:
            CURSOR.execute("""
                INSERT INTO users (username, email, password_hash, language, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (self.username, self.email, self.password_hash, self.language, self.created_at))
            self.id = CURSOR.lastrowid
        
        CONN.commit()
        return self

    def delete(self):
        if self.id:
            CURSOR.execute("DELETE FROM users WHERE id = ?", (self.id,))
            CONN.commit()
            self.id = None
            return True
        return False

    @classmethod
    def create(cls, username, email, password, language="en"):
        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = cls(username, email, password_hash, language)
        user.save()
        return user

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM users WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[0], row[5])
        return None

    @classmethod
    def find_by_username(cls, username):
        CURSOR.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = CURSOR.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[0], row[5])
        return None

    @classmethod
    def find_by_email(cls, email):
        CURSOR.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = CURSOR.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[0], row[5])
        return None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM users")
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0], row[5]) for row in rows]

    @classmethod
    def authenticate(cls, username, password):
        user = cls.find_by_username(username)
        if user:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if user.password_hash == password_hash:
                return user
        return None

    def get_children(self):
        from models.child import Child
        return Child.find_by_user_id(self.id)
