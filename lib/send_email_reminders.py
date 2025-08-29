import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, timedelta
from lib.db import get_db
from models.child_vaccine import ChildVaccine
from models.child import Child
from models.user import User

def send_email(to_email, subject, body, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

def send_vaccine_reminders():
    # Find all vaccines scheduled 3 days from today
    target_date = date.today() + timedelta(days=3)
    conn, cursor = get_db()
    cursor.execute("""
        SELECT cv.id, c.name, u.email, v.name, cv.scheduled_date
        FROM child_vaccines cv
        JOIN children c ON cv.child_id = c.id
        JOIN users u ON c.user_id = u.id
        JOIN vaccines v ON cv.vaccine_id = v.id
        WHERE cv.scheduled_date = ? AND cv.status = 'scheduled'
    """, (target_date,))
    reminders = cursor.fetchall()
    conn.close()
    for cv_id, child_name, user_email, vaccine_name, scheduled_date in reminders:
        subject = f"Vaccine Reminder: {vaccine_name} for {child_name}"
        body = f"This is a reminder that {child_name} is scheduled for the {vaccine_name} vaccine on {scheduled_date}."
        # Set your SMTP credentials here or use environment variables
        smtp_server = 'smtp.example.com'
        smtp_port = 587
        smtp_user = 'your_email@example.com'
        smtp_password = 'your_password'
        send_email(user_email, subject, body, smtp_server, smtp_port, smtp_user, smtp_password)
        print(f"Sent reminder to {user_email} for {child_name} - {vaccine_name} on {scheduled_date}")

if __name__ == "__main__":
    send_vaccine_reminders()
