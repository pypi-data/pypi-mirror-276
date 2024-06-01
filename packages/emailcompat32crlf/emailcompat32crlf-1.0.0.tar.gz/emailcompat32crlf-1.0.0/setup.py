# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='emailcompat32crlf',
      version='1.0.0',
      description='Patch stdlib email compat32 policy to default to CRLF line endings.',
      long_description=open('README.rst').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Communications :: Email',
      ],
      url='https://github.com/collective/emailcompat32crlf',
      author='Guido Stevens',
      author_email='guido.stevens@cosent.net',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)
