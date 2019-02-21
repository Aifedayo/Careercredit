import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__),os.pardir)))
setup(
    name='linuxjobber-Courses',
    version='1.2',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='An e-Learning application for grading.',
    long_description=README,
    url='',
    author='Ephraim J. , Louis E',
    author_email='ephraimjudgewell@gmail.com, louiseyoma@yahoo.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating system :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
        ]
    )

