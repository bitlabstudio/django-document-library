import os
from setuptools import setup, find_packages
import document_library


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-document-library",
    version=document_library.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, cms, documents, library, filer',
    author='Martin Brochhaus',
    author_email='mbrochh@gmail.com',
    url="https://github.com/bitmazk/django-document-library",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
        'django-hvad',
        'django-libs',
        'python-dateutil',
    ],
)
