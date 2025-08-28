from models import CONN, CURSOR
from datetime import datetime, date

class Child:
    def __init__(self, user_id, name, date_of_birth, gender, id=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"<Child {self.name} (DOB: {self.date_of_birth})>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Child's name must be at least 2 characters long")
        self._name = value.strip()

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Date of birth must be in YYYY-MM-DD format")
        
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        
        self._date_of_birth = value

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        valid_genders = ['male', 'female', 'other']
        if value.lower() not in valid_genders:
            raise ValueError(f"Gender must be one of: {', '.join(valid_genders)}")
        self._gender = value.lower()

    @property
    def age_in_months(self):
        today = date.today()
        age_delta = today - self.date_of_birth
        return age_delta.days // 30

    @property
    def age_in_years(self):
        today = date.today()
        age_delta = today - self.date_of_birth
        return age_delta.days // 365

    # ORM Methods
    def save(self):
        if self.id:
            CURSOR.execute("""
                UPDATE children 
                SET user_id = ?, name = ?, date_of_birth = ?, gender = ?
                WHERE id = ?
            """, (self.user_id, self.name, self.date_of_birth, self.gender, self.id))
        else:
            CURSOR.execute("""
                INSERT INTO children (user_id, name, date_of_birth, gender, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (self.user_id, self.name, self.date_of_birth, self.gender, self.created_at))
            self.id = CURSOR.lastrowid
        
        CONN.commit()
        return self

    def delete(self):
        if self.id:
            CURSOR.execute("DELETE FROM children WHERE id = ?", (self.id,))
            CONN.commit()
            self.id = None
            return True
        return False

    @classmethod
    def create(cls, user_id, name, date_of_birth, gender):
        child = cls(user_id, name, date_of_birth, gender)
        child.save()
        return child

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM children WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[0], row[5])
        return None

    @classmethod
    def find_by_user_id(cls, user_id):
        CURSOR.execute("SELECT * FROM children WHERE user_id = ?", (user_id,))
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0], row[5]) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM children WHERE name LIKE ?", (f"%{name}%",))
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0], row[5]) for row in rows]

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM children")
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0], row[5]) for row in rows]

    def get_user(self):
        from models.user import User
        return User.find_by_id(self.user_id)

    def get_vaccines(self):
        from models.child_vaccine import ChildVaccine
        return ChildVaccine.find_by_child_id(self.id)

    def get_upcoming_vaccines(self):
        from models.child_vaccine import ChildVaccine
        return ChildVaccine.find_upcoming_by_child_id(self.id)

    def get_overdue_vaccines(self):
        from models.child_vaccine import ChildVaccine
        return ChildVaccine.find_overdue_by_child_id(self.id)
