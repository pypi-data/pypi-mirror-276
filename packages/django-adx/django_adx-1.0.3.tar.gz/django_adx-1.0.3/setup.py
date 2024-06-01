import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-adx',
    version='v1.0.3',
    packages=find_packages(),
    include_package_data=True,
    license='GNU AGPL v3',
    # other arguments omitted
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/delcroip/django-adx',
    author='Patrick Delcroix',
    author_email='patrick.delcroix@swisstph.ch',
    install_requires=[
        'django',
        'dhis2.py',
        'pydantic',
        'dict2obj',
        'isodate',
        'python-dateutil',
        'numpy',
        'packaging'
    ],   
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
