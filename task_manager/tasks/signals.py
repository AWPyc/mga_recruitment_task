from django.db.models.signals import pre_save, post_save
from .models import Task, TaskHistory
from .serializers import TaskSerializer
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError
from django.db import DatabaseError

@receiver(pre_save, sender=Task)
def cache_old_task(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance.old = Task.objects.get(pk=instance.pk)
 
        except sender.DoesNotExist as e:
            instance.old = None

@receiver(post_save, sender=Task)
def create_task_history(sender, instance, created, **kwargs):
    if not created:
        try:
            old = getattr(instance, 'old')
            serializer = TaskSerializer()
            writable_fields = [field for field in serializer.Meta.fields if serializer.fields[field].read_only is False]

            for field in writable_fields:
                old_val = getattr(instance.old, field)
                new_val = getattr(instance, field)
                if old_val != new_val:
                    TaskHistory.objects.create(
                        task=old,
                        title=old.title,
                        description=old.description,
                        status=old.status,
                        assigned_to=getattr(old, 'assigned_to'),
                        owner=getattr(old, 'owner'),
                        history_user=getattr(instance, '_history_user')
                    )
                    break
    
        except DatabaseError as e:
            raise ValidationError(f'Cannot save Task history: {e}')
    