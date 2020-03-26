# Generated by Django 3.0.4 on 2020-03-23 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(default='xxx@126.com', max_length=255, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
