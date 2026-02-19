import os
import csv
from datetime import datetime, timedelta, timezone
from extensions import celery_app, db
from models import User, StudentProfile, PlacementDrive, Application
from flask import current_app

def send_mock_email(to, subject, body):
    """Utility to simulate sending an email/webhook without real SMTP credentials"""
    print(f"\n--- MOCK EMAIL ---")
    print(f"To: {to}\nSubject: {subject}\nBody:\n{body}")
    print(f"------------------\n")

@celery_app.task
def daily_deadline_reminders():
    """Scheduled Job - Daily reminders for upcoming application deadlines"""
    now = datetime.now(timezone.utc)
    upcoming_limit = now + timedelta(days=2) # Drives closing in next 48 hours
    
    closing_drives = PlacementDrive.query.filter(
        PlacementDrive.status == 'Approved',
        PlacementDrive.application_deadline > now,
        PlacementDrive.application_deadline <= upcoming_limit
    ).all()

    if not closing_drives:
        return "No upcoming deadlines."

    students = User.query.filter_by(role='Student', active_flag=True, blacklist_flag=False).all()
    
    for student in students:
        message = "Reminder: The following placement drives are closing soon:\n"
        for drive in closing_drives:
            message += f"- {drive.job_title} (Deadline: {drive.application_deadline.strftime('%Y-%m-%d')})\n"
        
        # Simulating Webhook/Email alert as required
        send_mock_email(to=student.username, subject="Upcoming Placement Deadlines", body=message)
        
    return "Daily reminders sent successfully."

@celery_app.task
def monthly_activity_report():
    """Scheduled Job - Monthly HTML Activity Report sent to Admin"""
    now = datetime.now(timezone.utc)
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Calculate stats
    drives_conducted = PlacementDrive.query.filter(PlacementDrive.created_at >= first_day_of_month).count()
    total_applied = Application.query.filter(Application.application_date >= first_day_of_month).count()
    total_selected = Application.query.filter(Application.application_date >= first_day_of_month, Application.status == 'Selected').count()

    html_report = f"""
    <html>
        <body>
            <h2>Monthly Placement Activity Report</h2>
            <p>Report for: {now.strftime('%B %Y')}</p>
            <ul>
                <li>Number of drives conducted: {drives_conducted}</li>
                <li>Number of students applied: {total_applied}</li>
                <li>Number of students selected: {total_selected}</li>
            </ul>
        </body>
    </html>
    """
    
    admin = User.query.filter_by(role='Admin').first()
    if admin:
        send_mock_email(to=admin.username, subject="Monthly Placement Activity Report", body=html_report)

    return "Monthly report generated and sent."

@celery_app.task
def export_applications_csv(student_id, username):
    """User Triggered Async Job - Export Applications as CSV"""
    applications = Application.query.filter_by(student_id=student_id).all()
    
    filename = f"export_{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = os.path.join(current_app.config['BASE_DIR'], 'uploads', filename)
    
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", "Company Name", "Drive Title", "Application Status", "Date Applied"])
        
        for app in applications:
            company_name = app.drive.company_profile.company_name if app.drive else "N/A"
            drive_title = app.drive.job_title if app.drive else "N/A"
            writer.writerow([
                app.student_id, 
                company_name, 
                drive_title, 
                app.status, 
                app.application_date.strftime('%Y-%m-%d')
            ])

    # Send alert once done
    send_mock_email(
        to=username, 
        subject="Your Application History Export is Ready", 
        body=f"Your CSV export is complete. File saved at: {filepath}"
    )
    
    return f"Export completed for {username}."