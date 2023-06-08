# Generated by Django 3.2.15 on 2023-05-31 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('languages', '0001_initial'),
        ('kpi', '0050_add_indexes_to_import_and_export_tasks'),
        ('markdownx_uploader', '0002_markdownxuploaderfilereference'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormDisclaimer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='')),
                ('default', models.BooleanField(default=False)),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disclaimers', to='kpi.asset')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='languages.language')),
            ],
            options={
                'verbose_name': 'global',
                'verbose_name_plural': 'global',
            },
        ),
        migrations.CreateModel(
            name='OverriddenFormDisclaimer',
            fields=[
            ],
            options={
                'verbose_name': 'per asset',
                'verbose_name_plural': 'per asset',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('form_disclaimer.formdisclaimer',),
        ),
        migrations.AddConstraint(
            model_name='formdisclaimer',
            constraint=models.UniqueConstraint(fields=('language', 'asset'), name='uniq_disclaimer_with_asset'),
        ),
        migrations.AddConstraint(
            model_name='formdisclaimer',
            constraint=models.UniqueConstraint(condition=models.Q(('asset', None)), fields=('language',), name='uniq_disclaimer_without_asset'),
        ),
    ]
