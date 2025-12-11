from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task()
def mail_task(email,otp):
    subject = 'OTP for Verify Account(CODERBOYS)'
    message = f'Assalomu aleykum CODERBOYS ecotizimida akkauntingizni faollashtirish/parolni qayta tiklash uchun kod {otp}\nKod 5 daqiqa amal qiladi'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,from_email,recipient_list)
    return f'Email jonatildi {email}'

