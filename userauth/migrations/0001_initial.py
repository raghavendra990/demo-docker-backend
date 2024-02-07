# Generated by Django 4.2.9 on 2024-02-05 19:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.UUIDField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.UUIDField(null=True)),
                ('id', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('phone_number', models.CharField(db_index=True, max_length=32, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlackListedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, max_length=500)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_user', to='userauth.usermodel')),
            ],
            options={
                'unique_together': {('token', 'user')},
            },
        ),
    ]
