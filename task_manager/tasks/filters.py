from .models import Task
import django_filters

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to']

class TaskHistoryFilter(django_filters.FilterSet):
    title = django_filters.ModelChoiceFilter(field_name="title", queryset=Task.objects.all())

    class Meta:
        model = Task
        fields = ['title']