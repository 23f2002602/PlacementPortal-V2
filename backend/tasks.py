from celery_worker import celery


@celery.task
def send_registration_email(email, name):


    print(f"Sending welcome email to {name} ({email})")


    return "email sent"




@celery.task
def send_application_notification(student, company):


    print(f"Notify {student} about application result from {company}")


    return "notification sent"