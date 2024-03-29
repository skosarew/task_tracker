# Generated by Django 2.2.5 on 2019-09-20 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Номер поставленной задачи')),
                ('status', models.CharField(choices=[('In Queue', 'Задача ждёт своей очереди на выполнение'), ('Run', 'Произошел запуск задачи'), ('Completed', 'Задача выполнена')], default='In Queue', max_length=100, verbose_name='Статус задачи')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Время создания задачи')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Время старта задачи')),
                ('exec_time', models.CharField(max_length=100, verbose_name='Время выполнения задачи')),
            ],
        ),
    ]
