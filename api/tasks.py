import os
import subprocess
import requests

from celery import shared_task
from django.conf import settings

from multiprocessing import Pool
from collections import deque

from api.models import Task

TASK_FILE_PATH = 'task.py'
START_URL = 'http://127.0.0.1:8000/{pk}/start/'
COMPLETE_URL = 'http://127.0.0.1:8000/{pk}/complete/'


@shared_task
def task_run(pk):
    url = START_URL.format(pk=pk)
    r = requests.post(url)
    task_file = os.path.join(settings.BASE_DIR, TASK_FILE_PATH)
    proc = subprocess.run(['python', task_file])
    url = COMPLETE_URL.format(pk=pk)
    r = requests.post(url)
    return proc.returncode


def task_run1(pk):
    url = START_URL.format(pk=pk)
    r = requests.post(url)
    import task
    url = COMPLETE_URL.format(pk=pk)
    r = requests.post(url)
    return r.status_code


# To be continued
def execute_all_task():
    num_workers = 2
    while True:
        queryset = Task.objects.all().filter(status="In Queue")
        task_queue = deque(queryset)

        while task_queue:
            p = Pool(num_workers)
            if len(task_queue) == 1:
                task = task_queue.popleft()
                print(p.map(task_run1, [task]))
            else:
                task_list = [task_queue.popleft() for _ in range(num_workers)]
                print(p.map(task_run1, task_list))
