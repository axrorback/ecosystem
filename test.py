import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from department.models import Department
from users.models import CustomUser
from django.db.models import Prefetch
from tasks.models import Task


# task = (
#     Task.objects
#     .select_related('department')
#     .prefetch_related('department__members')
#     .get(id=1509c19c-e5f1-40d2-978c-96abff7d928a)
# )




tasks = (Task.objects
        .select_related('department')
         .prefetch_related('department__members')
         .get(id='1509c19c-e5f1-40d2-978c-96abff7d928a')
         )
members = tasks.department.members.all()

for user in members:
    print(user.username, user.email)






# print(task)
#
# users = task.department.members.all()

# tas = Task.objects.first()
#
# print(tas.id)