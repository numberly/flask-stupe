from setuptools import setup


def get_description():
    with open("README.rst") as file:
        return file.read()


setup(
    name='Flask-Stupe',
    version='3.5.0',
    url='https://github.com/numberly/flask-stupe',
    license='MIT',
    author='Guillaume Gelin',
    author_email='ramnes@1000mercis.com',
    description='Flask application bootstrapping',
    long_description=get_description(),
    py_modules=['flask_stupe'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['Flask>=0.11'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
