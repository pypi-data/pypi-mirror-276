from pathlib import Path
from setuptools import setup, find_packages


contents = []
for filename in ("README.rst", "CHANGES.rst"):
    path = Path(filename)
    with path.open() as myfile:
        contents.append(myfile.read())
long_description = "\n\n".join(contents)

setup(name='emailcompat32crlf',
      version='1.0.3',
      description='Patch stdlib email compat32 policy to default to CRLF line endings.',
      long_description=long_description,
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
      zip_safe=False,
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """)
