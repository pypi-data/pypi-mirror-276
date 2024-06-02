
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='flask-interface-app',
    version='0.2.0',  
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-Bcrypt',
        'Flask-Login',
        'Flask-Admin',
        'email-validator'
    ],
    entry_points='''
        [console_scripts]
        create-flask-app=flask_interface_app.cli:create_flask_app
    ''',

    author="mdbaizidtanvir",
    author_email="mdbaizidtanvir@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/freebaizid/flask-interface',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

    # Set the title description
    description="flask-interface-app comes with a command-line interface (CLI) that mimics a bash terminal. It provides a CLI command to quickly generate a full file structure for a Flask app, along with a user-friendly bash-like UI for executing commands. and You can use it to execute various commands related to your Flask app.",
)




