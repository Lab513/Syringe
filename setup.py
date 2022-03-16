import pathlib
from setuptools import setup, find_packages

cyber = pathlib.Path(__file__).parent

README = (cyber / 'README.md').read_text()

setup(
    name='syringe',
    version='0.1',
    description='Push serynge',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Lionel Chiron',
    author_email='lchiron@curie.fr',
    url='',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
   ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
                       'pyserial',
                       'tqdm',
                       'flask-socketio==5.0.1',
                       'gevent',
                       'gevent-websocket',
                       'eventlet',
                       'oyaml'
                      ],

)
