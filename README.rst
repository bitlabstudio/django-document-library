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

Run the South migrations::

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



Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-document-library
    $ pip install -r requirements.txt
    $ ./logger/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    # Describe your change in the CHANGELOG.txt
    $ git add . && git commit
    $ git push origin feature_branch
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``tests/coverage/index.html``. When adding new features, please make sure that
you keep the coverage at 100%.


Roadmap
-------

Check the issue tracker on github for milestones and features to come.
