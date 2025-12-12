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


@shared_task
def new_mail(email, code, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    user = User.objects.get(id=user_id)

    subject = 'OTP for Verify NewEmail(CODERBOYS)'
    message = (
        f"Assalomu aleykum Hurmatli {user.username},\n"
        f"Siz emailingizni o'zgartirdingiz.\n"
        f"Yangi emailni tasdiqlash kodi: {code}\n"
        f"Kod 5 daqiqa amal qiladi."
    )

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

    return f"Yangi emailni tasdiqlash kodi {code} jo‘natildi"