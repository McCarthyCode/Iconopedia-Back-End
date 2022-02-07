# Generated by Django 4.0.1 on 2022-02-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='title',
            field=models.CharField(default='', max_length=80, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pdf',
            name='topic',
            field=models.PositiveSmallIntegerField(choices=[(1, 'About IconSyntax'), (2, 'Icon Diary'), (3, 'Icon Bookshelf')], default=3, verbose_name='Topic'),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='pdf',
            field=models.FileField(max_length=160, upload_to='pdf', verbose_name='PDF'),
        ),
    ]
