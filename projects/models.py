# from django.db import models
# from users.models import CustomUser
# from tasks.models import Task
# import uuid
# from django.core.validators import RegexValidator
#
# project_code_validator = RegexValidator(regex=r'^CB25PRJ-[0-9]{4}$',message='Project code formati CB25PRJ-0001 kabi bolishi kerak!')
#
# STATUS_CHOICES = (
#     ('done','Done'),
#     ('in_progress','In Progress'),
#     ('pending','Pending'),
#     ('cancelled','Cancelled'),
#     ('rejected','Rejected'),
#     ('approved','Approved'),
#     ('failed','Failed')
# )
#
#
# SERVER_STATUS_CHOICES = (
#     ('deployed','Deployed'),
#     ('not_deployed','Not Deployed'),
#     ('disabled','Disabled'),
#     ('active','Active'),
# )
#
# class Project(models.Model):
#     id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
#     code = models.CharField(max_length=15,unique=True,validators=[project_code_validator])
#     status_coding = models.CharField(max_length=12,choices=STATUS_CHOICES,default='pending')
#     status_deployment = models.CharField(max_length=12,choices=SERVER_STATUS_CHOICES,default='pending')
#     created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='created_projects')
#
