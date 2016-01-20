# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-18 00:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('family_tree', '0011_merge'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('comment', models.TextField(max_length=3000)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_set_for_comment', to='contenttypes.ContentType')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family_tree.Family')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family_tree.Person')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
