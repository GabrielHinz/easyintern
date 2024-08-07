# Generated by Django 4.2.13 on 2024-06-08 01:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('college', '0005_remove_collegeclass_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegeclass',
            name='teachers',
            field=models.ManyToManyField(blank=True, help_text='Professores responsáveis pela turma.', limit_choices_to={'type': 'teacher'}, related_name='teaching_classes', to=settings.AUTH_USER_MODEL, verbose_name='Professores'),
        ),
        migrations.AlterField(
            model_name='department',
            name='responsible',
            field=models.ForeignKey(blank=True, help_text='Professor responsável pelo departamento.', limit_choices_to={'type': 'teacher'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Responsável'),
        ),
    ]
