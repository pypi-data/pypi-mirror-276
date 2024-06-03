from setuptools import setup

description = "a place to list links + tools"

# :( `twine check` does not like the README
# because restructured text changed their tbale format
# https://sublime-and-sphinx-guide.readthedocs.io/en/latest/tables.html
#try:
#    description = open('README.txt').read()
#except IOError:
#    description = ''
long_description = description

version = "0.4.3"

# dependencies
dependencies = [
    'WebOb',
    'tempita',
    'paste',
    'pastescript', # technically optional, but here for ease of install
    'whoosh >= 2.5',
    'couchdb',
    'docutils',
    'pyloader',
    'theslasher',
    'pyes',
    ]

setup(name='toolk0s',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      author='Jeff Hammel',
      author_email='k0scist@gmail.com',
      url='http://k0s.org/hg/toolbox/',
      license="MPL",
      packages=['toolbox'],
      include_package_data=True,
      zip_safe=False,
      install_requires=dependencies,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      toolbox-convert-model = toolbox.model:convert
      toolbox-serve = toolbox.factory:main

      [paste.app_factory]
      toolbox = toolbox.factory:paste_factory
      """,
)
