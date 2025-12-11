# from django.db import models
# from users.models import CustomUser
#
# departments = (
#      ('front','Front End'),
#      ('back','Back End'),
#      ('fullstack','Full Stack'),
#      ('devops','DevOps'),
#      ('cicd','CI/CD'),
#      ('deploy','Deployment'),
#      ('others','Others'),
#      ('offtopic','Off Topic'),
# )
#
#
# class Group(models.Model):
#     name = models.CharField(max_length=100)
#     users = models.ManyToManyField(CustomUser,related_name='groups')
#     department = models.CharField(max_length=10,choices=departments)
#
#
#     def __str__(self):
#         return self.name
#
#
# class Meeting(models.Model):
#     group = models.ForeignKey(Group,on_delete=models.CASCADE)
#     topic = models.CharField(max_length=100)
#     date = models.DateTimeField()
#     purpose = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.topic
#
