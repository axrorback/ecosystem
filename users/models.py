import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
username_validator = RegexValidator(regex=r'^CB[0-9]{2}[A-Z]{3}[0-9]{3}$',message='Username formati CB24DEV001 kabi bolishi kerak!')
phone_validator = RegexValidator(regex=r'^\+998[0-9]{9}$',message='Telefon raqam faqat Ozbekiston regioni uchun amal qiladi! format (+998931004005 kbi kiriting)')

roles = (
    ('super','SuperAdmin'),
    ('manager','Manager'),
    ('simpleuser','SimpleUser'),
    ('dev','Developer'),
)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username = models.CharField(max_length=15,unique=True,validators=[username_validator],verbose_name='Username')
    phone_number = models.CharField(max_length=13,unique=True,validators=[phone_validator],blank=True,null=True,verbose_name='Phone number')
    telegram_id = models.CharField(max_length=13,blank=True,null=True,verbose_name='Telegram ID')
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=10,choices=roles,default='simpleuser')
    is_2fa_enabled = models.BooleanField(default=False)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

purpose = (
    ('verify','Verify Account'),
    ('forgot','OTP for Restore Account Password'),
)

class OTP(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=10,choices=purpose)

    def __str__(self):
        return f'{self.user.username}-{self.purpose}-{self.otp}'

class TwoFactorOTP(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

class PendingEmailChange(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    new_email = models.EmailField(verbose_name='New Email'),
    code = models.CharField(max_length=10,verbose_name='Verification Code')
    created_at = models.DateTimeField(auto_now_add=True)