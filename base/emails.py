from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email, email_token, purpose="activation"):
    if purpose == "activation":
        subject = "Your account needs to be verified"
        message = f"""
Dear User,  

Thank you for registering with us. To complete your account setup and verify your email address, please click the link below:  

🔗 http://127.0.0.1:8000/accounts/activate/{email_token} 

If you did not create this account, please ignore this email.  

Best regards,  
MYBRAND
"""
    elif purpose == "password_reset":
        subject = "Password Reset Request"
        message = f"""
Dear User,  

We received a request to reset your password. If you made this request, please click the link below to reset your password:  

🔗 http://127.0.0.1:8000/accounts/reset-password/{email_token}  

If you did not request this, please ignore this email.  

Best regards,  
MYBRAND
"""
    
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])