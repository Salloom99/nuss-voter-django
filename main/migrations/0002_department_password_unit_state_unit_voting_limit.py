# Generated by Django 4.0.2 on 2022-02-13 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='password',
            field=models.CharField(default='1234567890', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unit',
            name='state',
            field=models.CharField(choices=[('A', 'Active'), ('S', 'Suspended'), ('F', 'Finished')], default='S', max_length=1),
        ),
        migrations.AddField(
            model_name='unit',
            name='voting_limit',
            field=models.PositiveSmallIntegerField(default=24),
        ),
    ]
