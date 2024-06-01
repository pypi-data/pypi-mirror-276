# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='emailcompat32crlf',
      version='1.0.2',
      description='Patch stdlib email compat32 policy to default to CRLF line endings.',
      long_description=open('README.rst').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Topic :: Communications :: Email',
      ],
      url='https://github.com/collective/emailcompat32crlf',
      keywords=["email"],
      author='Guido Stevens',
      author_email='guido.stevens@cosent.net',
      license='MIT',
      python_requires=">=3.8",
      packages=find_packages(),
      zip_safe=False)
