from setuptools import setup

setup(
    name='synthia',
    packages=['core', 'web'],
    include_package_data=True,
    install_requires=[
        # core
        'sqlalchemy',
        'psycopg2-binary',
        # web
        'flask',
        'flasgger',
        'marshmallow',
        'apispec',
        'flask_cors'
    ],
)
