# encoding: utf-8
try:
    from setuptools import setup
except ImportError:
    # For Python 3.12+, setuptools is no longer in stdlib
    import sys
    print("Error: setuptools is required but not found.")
    print("Please install setuptools package using:")
    print("pip install setuptools")
    sys.exit(1)


def get_description():
    with open("README.rst") as file:
        return file.read()


setup(
    name='Flask-Stupe',
    version='4.4.0',
    url='https://github.com/numberly/flask-stupe',
    license='MIT',
    author='Guillaume Gelin',
    author_email='1m_rtb_devops@numberly.com',
    description='a.k.a. « Flask on steroids »',
    long_description=get_description(),
    packages=['flask_stupe'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.8',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
