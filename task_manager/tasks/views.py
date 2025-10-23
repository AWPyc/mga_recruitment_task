from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TaskSerializer, TaskHistorySummarySerializer, TaskDetailSerializer
from .models import Task
from .filters import TaskFilter, TaskHistoryFilter
from rest_framework.response import Response
from django.db import transaction
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.instance._history_user = self.request.user
        return super().perform_update(serializer)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TaskDetailSerializer(instance)   
        return Response(serializer.data)


class TaskHistoryViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-updated_at')
    serializer_class = TaskHistorySummarySerializer
    filterset_class = TaskHistoryFilter
    http_method_names = ['get']
    