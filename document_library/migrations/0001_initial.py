# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import filer.fields.folder
from django.conf import settings
import filer.fields.image
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0013_urlconfrevision'),
        ('filer', '0002_auto_20150606_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='Position', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('position', models.PositiveIntegerField(null=True, verbose_name='Position', blank=True)),
                ('is_on_front_page', models.BooleanField(default=False, verbose_name='Is on front page')),
                ('source_url', models.URLField(help_text='Use this if you want to give credit for a downloadable file.', verbose_name='Source URL', blank=True)),
                ('download_url', models.URLField(help_text='Use this if you want to link to a file instead of self-hosting it', verbose_name='Download URL', blank=True)),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('document_date', models.DateTimeField(null=True, verbose_name='Document date', blank=True)),
            ],
            options={
                'ordering': ('position', '-document_date'),
            },
        ),
        migrations.CreateModel(
            name='DocumentCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('slug', models.SlugField(max_length=32, verbose_name='Slug')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentCategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='document_library.DocumentCategory', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'document_library_documentcategory_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='DocumentTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Short description', blank=True)),
                ('copyright_notice', models.CharField(max_length=1024, verbose_name='Copyright notice', blank=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published')),
                ('meta_description', models.TextField(max_length=512, verbose_name='Meta description', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('filer_file', filer.fields.file.FilerFileField(related_name='document_files', verbose_name='File', blank=True, to='filer.File', null=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='document_library.Document', null=True)),
                ('thumbnail', filer.fields.file.FilerFileField(related_name='document_thumbnails', verbose_name='Thumbnail', blank=True, to='filer.File', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'document_library_document_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='document',
            name='category',
            field=models.ForeignKey(verbose_name='Category', blank=True, to='document_library.DocumentCategory', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='content',
            field=cms.models.fields.PlaceholderField(related_name='documents', slotname='document_library_content', editable=False, to='cms.Placeholder', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='folder',
            field=filer.fields.folder.FilerFolderField(related_name='document_folders', verbose_name='Folder', blank=True, to='filer.Folder', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='image',
            field=filer.fields.image.FilerImageField(related_name='document_images', verbose_name='Image', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='document',
            field=models.ForeignKey(verbose_name='Document', to='document_library.Document'),
        ),
        migrations.AlterUniqueTogether(
            name='documenttranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentcategorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
