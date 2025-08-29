from ..db import get_db
from datetime import datetime

class Vaccine:
    def __init__(self, name, description, recommended_age_months, dose_number=1, is_required=True, id=None, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.recommended_age_months = recommended_age_months
        self.dose_number = dose_number
        self.is_required = is_required
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"<Vaccine {self.name} ({self.recommended_age_months} months, Dose {self.dose_number})>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("Vaccine name must be at least 3 characters long")
        self._name = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value or len(value.strip()) < 10:
            raise ValueError("Vaccine description must be at least 10 characters long")
        self._description = value.strip()

    @property
    def recommended_age_months(self):
        return self._recommended_age_months

    @recommended_age_months.setter
    def recommended_age_months(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Recommended age must be a positive integer")
        self._recommended_age_months = value

    @property
    def dose_number(self):
        return self._dose_number

    @dose_number.setter
    def dose_number(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Dose number must be a positive integer")
        self._dose_number = value

    @property
    def is_required(self):
        return self._is_required

    @is_required.setter
    def is_required(self, value):
        # Handle both boolean and integer values (SQLite stores booleans as integers)
        if isinstance(value, bool):
            self._is_required = value
        elif isinstance(value, int):
            self._is_required = bool(value)
        else:
            raise ValueError("is_required must be a boolean or integer value")

    # ORM Methods
    def save(self):
        conn, cursor = get_db()
        if self.id:
            cursor.execute("""
                UPDATE vaccines 
                SET name = ?, description = ?, recommended_age_months = ?, dose_number = ?, is_required = ?
                WHERE id = ?
            """, (self.name, self.description, self.recommended_age_months, self.dose_number, self.is_required, self.id))
        else:
            cursor.execute("""
                INSERT INTO vaccines (name, description, recommended_age_months, dose_number, is_required, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.name, self.description, self.recommended_age_months, self.dose_number, self.is_required, self.created_at))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    def delete(self):
        if self.id:
            conn, cursor = get_db()
            cursor.execute("DELETE FROM vaccines WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()
            self.id = None
            return True
        return False

    @classmethod
    def create(cls, name, description, recommended_age_months, dose_number=1, is_required=True):
        vaccine = cls(name, description, recommended_age_months, dose_number, is_required)
        vaccine.save()
        return vaccine

    @classmethod
    def find_by_id(cls, id):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM vaccines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[5], row[0], row[6])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM vaccines WHERE name LIKE ?", (f"%{name}%",))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[0], row[6]) for row in rows]

    @classmethod
    def find_by_age_months(cls, age_months):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM vaccines WHERE recommended_age_months <= ? ORDER BY recommended_age_months", (age_months,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[0], row[6]) for row in rows]

    @classmethod
    def find_required(cls):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM vaccines WHERE is_required = 1 ORDER BY recommended_age_months")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[0], row[6]) for row in rows]

    @classmethod
    def get_all(cls):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM vaccines ORDER BY recommended_age_months")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[0], row[6]) for row in rows]

    def get_child_vaccines(self):
        from models.child_vaccine import ChildVaccine
        return ChildVaccine.find_by_vaccine_id(self.id)
