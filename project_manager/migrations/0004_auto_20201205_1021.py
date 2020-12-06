# Generated by Django 3.1.4 on 2020-12-05 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0003_delete_geeksmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='avatar',
            field=models.ImageField(upload_to=''),
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.DateField()),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='date start')),
                ('end_date', models.DateField(verbose_name='date end')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.project')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
