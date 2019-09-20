import rest_framework

from .models import Task


class TaskSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

