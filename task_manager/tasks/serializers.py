from rest_framework import serializers
from .models import Task, TaskHistory
from django.contrib.auth.models import User
from collections import OrderedDict

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(many=False, allow_null=True, queryset=User.objects.all(), write_only=True)
    assigned_user = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'owner', 'title', 'description', 'status', 'created_at', 'updated_at', 'assigned_to', 'assigned_user']

    def to_representation(self, instance):
        result = super(TaskSerializer, self).to_representation(instance)
        hidden_fields = ['created_at', 'updated_at', 'assigned_to', 'owner']
        return OrderedDict([(key, val) for key, val in result.items() if key not in hidden_fields])

    def get_assigned_user(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.username
        return 'No user assigned'


class TaskDetailSerializer(serializers.ModelSerializer):
    assigned_user = serializers.SerializerMethodField()
    owner_user = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_user', 'assigned_to', 
        'owner_user', 'owner', 'created_at', 'updated_at']

    def get_owner_user(self, obj):
        return obj.owner.username

    def get_assigned_user(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.username
        return "No user assigned"


class TaskHistorySummarySerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()
    history = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'history']

    def get_history(self, obj):
        task_history = obj.history.all()
        print(task_history)
        return TaskHistorySerializer(task_history, many=True).data


class TaskHistorySerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(many=False, queryset=Task.objects.all(), write_only=True)
    assigned_user = serializers.SerializerMethodField()
    history_user_username = serializers.SerializerMethodField()

    class Meta:
        model = TaskHistory
        fields = ['task', 'title', 'description', 'status', 'assigned_user', 'assigned_to', 'changed_on', 
            'history_user_username', 'history_user']

    def get_assigned_user(self, obj):
        if not obj.assigned_to:
            return "No user assigned"
        return obj.assigned_to.username
    
    def get_history_user_username(self, obj):
        return obj.history_user.username