# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(unique=True, max_length=250)),
                ('published', models.DateField(null=True, blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'Time Updated')),
                ('content', models.TextField(help_text=b'Use Markdown syntax.', verbose_name=b'Page body')),
                ('parent', models.ForeignKey(to='dmcm.Page', null=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
