from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    STATUS_CHOICES = {
        'new': 'New',
        'in_progress': 'In progress',
        "resolved": 'Resolved',
    }
    
    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField(null=False, default='No description provided.')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=False, default=STATUS_CHOICES.get('new'))
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_tasks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_tasks', null=True)

    def __str__(self):
        return self.title


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history", null=False)
    title = models.TextField(max_length=30, null=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=15, choices=Task.STATUS_CHOICES, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="history_assigned_to", null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="history_owner", null=True)
    history_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="history_user", null=True)
    changed_on = models.DateTimeField(auto_now=True)
