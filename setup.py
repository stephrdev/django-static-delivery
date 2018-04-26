import os
from codecs import open

from setuptools import setup, find_packages


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION = __import__('static_delivery').__version__


with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-static-delivery',
    version=VERSION,
    description='A middleware to delivery static files in Django.',
    long_description=long_description,
    url='https://github.com/moccu/django-static-delivery',
    project_urls={
        'Bug Reports': 'https://github.com/moccu/django-static-delivery/issues',
        'Source': 'https://github.com/moccu/django-delivery',
    },
    author='Stephan Jaekel',
    author_email='steph@rdev.info',
    packages=find_packages(exclude=['docs', 'tests', 'tests.*']),
    install_requires=[],
    include_package_data=True,
    keywords='django staticfiles',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
