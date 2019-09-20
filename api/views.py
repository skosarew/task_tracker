from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timezone
import pandas as pd

from .models import Task
from .serializers import TaskSerializer
from .tasks import task_run, execute_all_task
from .settings import API_VERSION


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(methods=['post', 'get'], detail=False, url_path='create', url_name='create')
    def create_task(self, request):
        task = Task()
        task.save()
        if API_VERSION == 2:
            task_run.delay(task.pk)
        elif API_VERSION == 1:
            execute_all_task()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='status', url_name='status')
    def status_task(self, request, pk=None):
        """
        <pk>/status/
        """
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=404,
                            data=dict(details='There is no task with this number'))
        return Response(status=200,
                        data=task.status)

    @action(methods=['post'], detail=True, url_path='start', url_name='start')
    def start_task(self, request, pk=None):
        """
        <pk>/start/
        """
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=404,
                            data=dict(details='There is no task with this number'))
        if task.status != Task.IN_QUEUE:
            return Response(status=400,
                            data=dict(details='The task has already been started'))

        task.status = Task.RUN
        task.start_time = pd.datetime.now()
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='complete', url_name='complete')
    def complete_task(self, request, pk=None):
        """
        <pk>/complete/
        """
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=404,
                            data=dict(details='There is no task with this number'))
        if task.status != Task.RUN:
            return Response(status=400,
                            data=dict(details='Task cannot be completed'))
        task.status = Task.COMPLETED
        now = datetime.now(timezone.utc)
        task.exec_time = str(pd.to_timedelta(now - task.start_time))
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)
