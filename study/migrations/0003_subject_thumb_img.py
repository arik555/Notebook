# Generated by Django 2.1.7 on 2019-03-31 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_auto_20190331_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='thumb_img',
            field=models.URLField(blank=True),
        ),
    ]
