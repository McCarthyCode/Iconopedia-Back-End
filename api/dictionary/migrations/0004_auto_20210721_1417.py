# Generated by Django 3.2.3 on 2021-07-21 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_auto_20210707_2336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='icon',
            name='part_speech',
        ),
        migrations.RemoveField(
            model_name='icon',
            name='tense',
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='datetime created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='datetime updated')),
                ('name', models.CharField(max_length=40)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='dictionary.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='icon',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionary.category'),
        ),
    ]
