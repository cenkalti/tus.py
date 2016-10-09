# coding=utf-8
from setuptools import setup

setup(
    name='tus.py',
    description='tus (resumable file upload protocol) client',
    version='1.0.1',
    author=u'Cenk Altı',
    author_email='cenkalti@gmail.com',
    url='https://github.com/cenk/tus.py',
    py_modules=['tus'],
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'tus-upload = tus:_cmd_upload',
            'tus-resume = tus:_cmd_resume',
        ],
    },
)
