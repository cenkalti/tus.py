# coding=utf-8
from setuptools import setup

setup(
    name='tus.py',
    description='tus (resumable file upload protocol) client',
    version='1.1.0',
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
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
