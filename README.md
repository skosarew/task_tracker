# Task_tracker
Web service prototype for organizing the task queue.

### Initialization
Run the following in terminal:

python manage.py runserver

celery worker -A queue_project --loglevel=debug --concurrency=2

### To verify execution  
http://127.0.0.1:8000/ - to inspect the queue

http://127.0.0.1:8000/create/ - to create new task

http://127.0.0.1:8000/n/ - to inspect the status of task n