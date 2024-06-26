# Generated by Django 5.0.3 on 2024-03-05 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('social_django', '0015_rename_extra_data_new_usersocialauth_extra_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_auth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_django.usersocialauth')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instagram.customuser')),
            ],
        ),
    ]
