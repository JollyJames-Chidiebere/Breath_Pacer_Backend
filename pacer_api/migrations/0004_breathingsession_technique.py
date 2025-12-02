# Generated migration for adding technique field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacer_api', '0003_breathplan_exhale_hold_ms'),
    ]

    operations = [
        migrations.AddField(
            model_name='breathingsession',
            name='technique',
            field=models.CharField(blank=True, default='Breathing 2(Oscilloscope)', max_length=128),
        ),
    ]

