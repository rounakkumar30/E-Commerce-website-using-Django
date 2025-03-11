from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email, email_token):
    subject = "Your account needs to be verified"
    email_from = settings.EMAIL_HOST_USER
    message = f"""
Dear User,  

Thank you for registering with us. To complete your account setup and verify your email address, please click the link below:  

🔗 http://127.0.0.1:8000/accounts/activate/{email_token} 

If you did not create this account, please ignore this email.  

Best regards,  
MYBRAND
"""

    
    send_mail(subject, message, email_from, [email])
