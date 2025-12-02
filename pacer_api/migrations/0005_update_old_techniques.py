# Migration to clear technique field for old sessions

from django.db import migrations


def clear_old_techniques(apps, schema_editor):
    BreathingSession = apps.get_model('pacer_api', 'BreathingSession')
    # Update all sessions with "Breathing 2(Oscilloscope)" to blank
    BreathingSession.objects.filter(technique="Breathing 2(Oscilloscope)").update(technique="")


class Migration(migrations.Migration):

    dependencies = [
        ('pacer_api', '0004_breathingsession_technique'),
    ]

    operations = [
        migrations.RunPython(clear_old_techniques),
    ]
