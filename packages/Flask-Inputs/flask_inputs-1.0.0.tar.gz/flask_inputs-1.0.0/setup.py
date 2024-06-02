
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

if not path.exists('README.rst'):
    import pypandoc
    pypandoc.download_pandoc(targetfolder='~/bin/')
    pypandoc.convert_file('README.md', 'rst', outputfile='README.rst')

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    python_requires='>=3.9',
    name='Flask-Inputs',
    version='1.0.0',
    description='Flask request data validation',
    long_description=long_description,
    url='http://pythonhosted.org/Flask-Inputs',
    author='David Parker',
    author_email='durera@gmail.com',
    license='MIT',
    keywords='flask validation wtforms',
    package_dir={'': 'src'},
    packages=['flask_inputs'],
    install_requires=[
        'flask >= 3',
        'wtforms >= 3',
        'future >= 1'
    ],
    extras_require={
        'dev': [
            'build',
            'pytest',
            'email_validator',
            'jsonschema'
        ]
    },
)
