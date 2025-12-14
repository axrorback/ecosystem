from django.db import models
import uuid
from users.models import CustomUser
from django.core.validators import RegexValidator
from django.conf import settings
department_code_validator = RegexValidator(r'^CB[0-9]{2}[A-Z]{3}-DEPT$',message='Department code formati CB24AIM-DEPT kabi bolishi kerak!')


class Department(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    code = models.CharField(max_length=15,unique=True,validators=[department_code_validator])
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='created_departments')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code}-{self.name}'