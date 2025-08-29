from lib.db import get_db
from datetime import datetime, date, timedelta

class ChildVaccine:
    def __init__(self, child_id, vaccine_id, scheduled_date, completed_date=None, status="scheduled", reminder_sent=False, id=None, created_at=None):
        self.id = id
        self.child_id = child_id
        self.vaccine_id = vaccine_id
        self.scheduled_date = scheduled_date
        self.completed_date = completed_date
        self.status = status
        self.reminder_sent = reminder_sent
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"<ChildVaccine {self.child_id}-{self.vaccine_id} ({self.status})>"

    @property
    def scheduled_date(self):
        return self._scheduled_date

    @scheduled_date.setter
    def scheduled_date(self, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Scheduled date must be in YYYY-MM-DD format")
        
        if value < date.today():
            raise ValueError("Scheduled date cannot be in the past")
        
        self._scheduled_date = value

    @property
    def completed_date(self):
        return self._completed_date

    @completed_date.setter
    def completed_date(self, value):
        if value is not None:
            if isinstance(value, str):
                try:
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError("Completed date must be in YYYY-MM-DD format")
            
            if value > date.today():
                raise ValueError("Completed date cannot be in the future")
        
        self._completed_date = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        valid_statuses = ['scheduled', 'completed', 'overdue']
        if value.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        self._status = value.lower()

    @property
    def reminder_sent(self):
        return self._reminder_sent

    @reminder_sent.setter
    def reminder_sent(self, value):
        # Handle both boolean and integer values (SQLite stores booleans as integers)
        if isinstance(value, bool):
            self._reminder_sent = value
        elif isinstance(value, int):
            self._reminder_sent = bool(value)
        else:
            raise ValueError("reminder_sent must be a boolean or integer value")

    @property
    def is_overdue(self):
        if self.status == 'completed':
            return False
        return self.scheduled_date < date.today()

    @property
    def days_until_due(self):
        if self.status == 'completed':
            return 0
        delta = self.scheduled_date - date.today()
        return delta.days

    @property
    def is_due_soon(self):
        return 0 <= self.days_until_due <= 7

    # ORM Methods
    def save(self):
        conn, cursor = get_db()
        if self.id:
            cursor.execute("""
                UPDATE child_vaccines 
                SET child_id = ?, vaccine_id = ?, scheduled_date = ?, completed_date = ?, 
                    status = ?, reminder_sent = ?
                WHERE id = ?
            """, (self.child_id, self.vaccine_id, self.scheduled_date, self.completed_date, 
                  self.status, self.reminder_sent, self.id))
        else:
            cursor.execute("""
                INSERT INTO child_vaccines (child_id, vaccine_id, scheduled_date, completed_date, 
                                          status, reminder_sent, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.child_id, self.vaccine_id, self.scheduled_date, self.completed_date, 
                  self.status, self.reminder_sent, self.created_at))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    def delete(self):
        if self.id:
            conn, cursor = get_db()
            cursor.execute("DELETE FROM child_vaccines WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()
            self.id = None
            return True
        return False

    def mark_completed(self, completed_date=None):
        if completed_date is None:
            completed_date = date.today()
        
        self.completed_date = completed_date
        self.status = 'completed'
        self.save()
        return self

    def mark_overdue(self):
        if self.status != 'completed':
            self.status = 'overdue'
            self.save()
        return self

    @classmethod
    def create(cls, child_id, vaccine_id, scheduled_date):
        child_vaccine = cls(child_id, vaccine_id, scheduled_date)
        child_vaccine.save()
        return child_vaccine

    @classmethod
    def find_by_id(cls, id):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM child_vaccines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0], row[7])
        return None

    @classmethod
    def find_by_child_id(cls, child_id):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM child_vaccines WHERE child_id = ? ORDER BY scheduled_date", (child_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0], row[7]) for row in rows]

    @classmethod
    def find_by_vaccine_id(cls, vaccine_id):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM child_vaccines WHERE vaccine_id = ? ORDER BY scheduled_date", (vaccine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0], row[7]) for row in rows]

    @classmethod
    def find_upcoming_by_child_id(cls, child_id):
        conn, cursor = get_db()
        cursor.execute("""
            SELECT * FROM child_vaccines 
            WHERE child_id = ? AND status = 'scheduled' AND scheduled_date >= ?
            ORDER BY scheduled_date
        """, (child_id, date.today()))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0], row[7]) for row in rows]

    @classmethod
    def find_overdue_by_child_id(cls, child_id):
        conn, cursor = get_db()
        cursor.execute("""
            SELECT * FROM child_vaccines 
            WHERE child_id = ? AND status != 'completed' AND scheduled_date < ?
            ORDER BY scheduled_date
        """, (child_id, date.today()))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0], row[7]) for row in rows]

    @classmethod
    def find_due_soon(cls, days=7):
        target_date = date.today() + timedelta(days=days)
        conn, cursor = get_db()
        cursor.execute("""
            SELECT * FROM child_vaccines 
            WHERE status = 'scheduled' AND scheduled_date <= ? AND scheduled_date >= ?
            ORDER BY scheduled_date
        """, (target_date, date.today()))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0], row[7]) for row in rows]

    @classmethod
    def get_all(cls):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM child_vaccines ORDER BY scheduled_date")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0], row[7]) for row in rows]

    def get_child(self):
        from models.child import Child
        return Child.find_by_id(self.child_id)

    def get_vaccine(self):
        from models.vaccine import Vaccine
        return Vaccine.find_by_id(self.vaccine_id)

    def get_reminders(self):
        from models.reminder import Reminder
        return Reminder.find_by_child_vaccine_id(self.id)
