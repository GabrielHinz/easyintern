# Generated by Django 4.2.13 on 2024-06-08 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0005_remove_collegeclass_students'),
        ('users', '0005_usercustom_student_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercustom',
            name='comapany_sector',
            field=models.CharField(blank=True, help_text='Setor da empresa.', max_length=64, null=True, verbose_name='Setor'),
        ),
        migrations.AddField(
            model_name='usercustom',
            name='company_cnpj',
            field=models.CharField(blank=True, help_text='CNPJ da empresa.', max_length=14, null=True, verbose_name='CNPJ'),
        ),
        migrations.AlterField(
            model_name='usercustom',
            name='student_class',
            field=models.ForeignKey(blank=True, help_text='Turma do aluno.', null=True, on_delete=django.db.models.deletion.CASCADE, to='college.collegeclass', verbose_name='Turma'),
        ),
    ]
