Django Document Library
=======================

A Django application to manage multilingual documents and display them on your
site in a downloads section.

Comes with a django-cms apphook and is based on django-filer.


Installation
------------

If you want to install the latest stable release from PyPi::

    $ pip install django-document-library

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-document-library.git#egg=document_library

Add ``document_library`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'document_library',
    )

Run the migrations::

    ./manage.py migrate document_library


Admin inline
------------

You can attach documents to any model. To make things easier, you can add
a tabular inline to your model's admin which allows to attach documents.

In your project's ``models.py`` or any file that get's loaded early, do the
following::

    from yourapp.admin import YourAdmin
    from object_attachments.admin import ObjectAttachmentInline

    YourAdmin.inlines = YourAdmin.inlines[:] + [ObjectAttachmentInline]


Templatetags
------------


get_files_for_documents
+++++++++++++++++++++++

Use this templatetag in order to render all files for a given document::

    {% load document_library_tags %}
    {% get_files_for_document document as files %}
    {% for file in files %}
        <p><a href="{{ file.url }}">{{ file.name|default:file.original_filename }}</a></p>
    {% endfor %}


get_frontpage_documents
+++++++++++++++++++++++

Use this templatetag if you want to render a list of documents on your
frontpage::

    {% load document_library_tags %}
    {% get_frontpage_documents as documents %}
    <ul>
        {% for document in documents %}
            <li><a href="/url/to/library/">{{ document.get_title }}</a></li>
        {% endfor %}
    </ul>


Settings
--------

DOCUMENT_LIBRARY_LOGIN_REQUIRED
+++++++++++++++++++++++++++++++

Default: ``False``

Set this to ``True`` if you wand to require login for the views of this app.


DOCUMENT_LIBRARY_PAGINATION_AMOUNT
++++++++++++++++++++++++++++++++++

Default: 1

Amount of documents display on one page.


DOCUMENT_LIBRARY_PAGINATE_BY_CATEGORIES
+++++++++++++++++++++++++++++++++++++++

Default: False

Enables a special ordering of the document list to always show an equal amount
of documents for each category.


Sitemaps
++++++++

To add a sitemap of your documents, add the following to your urlconf: ::

    from document_library.sitemaps import DocumentSitemap

    urlpatterns += patterns(
        '',
        url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {
            'sitemaps': {
                'documents': DocumentSitemap,
            }, }),
    )


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-document-library
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.8 and Django 1.9) and run the tests against both
environments.
