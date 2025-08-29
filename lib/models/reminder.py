from ..db import get_db
from datetime import datetime, date

class Reminder:
    def __init__(self, child_vaccine_id, reminder_date, message, sent=False, id=None, created_at=None):
        self.id = id
        self.child_vaccine_id = child_vaccine_id
        self.reminder_date = reminder_date
        self.message = message
        self.sent = sent
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"<Reminder {self.id} for {self.child_vaccine_id} on {self.reminder_date}>"

    @property
    def reminder_date(self):
        return self._reminder_date

    @reminder_date.setter
    def reminder_date(self, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Reminder date must be in YYYY-MM-DD format")
        
        if value < date.today():
            raise ValueError("Reminder date cannot be in the past")
        
        self._reminder_date = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if not value or len(value.strip()) < 5:
            raise ValueError("Reminder message must be at least 5 characters long")
        self._message = value.strip()

    @property
    def sent(self):
        return self._sent

    @sent.setter
    def sent(self, value):
        # Handle both boolean and integer values 
        if isinstance(value, bool):
            self._sent = value
        elif isinstance(value, int):
            self._sent = bool(value)
        else:
            raise ValueError("Sent must be a boolean or integer value")

    @property
    def is_due(self):
        return self.reminder_date <= date.today() and not self.sent

    # ORM Methods
    def save(self):
        conn, cursor = get_db()
        if self.id:
            cursor.execute("""
                UPDATE reminders 
                SET child_vaccine_id = ?, reminder_date = ?, message = ?, sent = ?
                WHERE id = ?
            """, (self.child_vaccine_id, self.reminder_date, self.message, self.sent, self.id))
        else:
            cursor.execute("""
                INSERT INTO reminders (child_vaccine_id, reminder_date, message, sent, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (self.child_vaccine_id, self.reminder_date, self.message, self.sent, self.created_at))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    def delete(self):
        if self.id:
            conn, cursor = get_db()
            cursor.execute("DELETE FROM reminders WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()
            self.id = None
            return True
        return False



    @classmethod
    def create(cls, child_vaccine_id, reminder_date, message):
        reminder = cls(child_vaccine_id, reminder_date, message)
        reminder.save()
        return reminder

    @classmethod
    def find_by_id(cls, id):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM reminders WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[1], row[2], row[3], row[4], row[0], row[5])
        return None

    @classmethod
    def find_by_child_vaccine_id(cls, child_vaccine_id):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM reminders WHERE child_vaccine_id = ? ORDER BY reminder_date", (child_vaccine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[0], row[5]) for row in rows]

    @classmethod
    def find_due_reminders(cls):
        conn, cursor = get_db()
        cursor.execute("""
            SELECT * FROM reminders 
            WHERE reminder_date <= ? AND sent = 0
            ORDER BY reminder_date
        """, (date.today(),))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[0], row[5]) for row in rows]

    @classmethod
    def find_upcoming_reminders(cls, days=7):
        from datetime import timedelta
        target_date = date.today() + timedelta(days=days)
        conn, cursor = get_db()
        cursor.execute("""
            SELECT * FROM reminders 
            WHERE reminder_date <= ? AND reminder_date >= ? AND sent = 0
            ORDER BY reminder_date
        """, (target_date, date.today()))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[0], row[5]) for row in rows]

    @classmethod
    def get_all(cls):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM reminders ORDER BY reminder_date")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row[1], row[2], row[3], row[4], row[0], row[5]) for row in rows]

    def get_child_vaccine(self):
        from models.child_vaccine import ChildVaccine
        return ChildVaccine.find_by_id(self.child_vaccine_id)

    def get_child(self):
        child_vaccine = self.get_child_vaccine()
        if child_vaccine:
            return child_vaccine.get_child()
        return None

    def get_vaccine(self):
        child_vaccine = self.get_child_vaccine()
        if child_vaccine:
            return child_vaccine.get_vaccine()
        return None
