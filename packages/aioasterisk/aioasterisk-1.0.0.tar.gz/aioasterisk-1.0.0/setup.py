from setuptools import setup
from textwrap import dedent

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='aioasterisk',
      version='1.0.0',
      packages=['aioasterisk'],
      description='Async Python library for interacting with the Asterisk FreePBX',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://www.asterisk.org/',
      download_url='https://github.com/developerreva/aioasterisk',
      keywords='python python3 api-client aiohttp api-wrapper asterisk asterisk-api asterisk-async',
      license='BSD License',
      author='Developereva',
      author_email='developereva@protonmail.com',
      project_urls={
        'Source Code': 'https://github.com/developerreva/aioasterisk',
        'Documentation': 'https://github.com/developerreva/aioasterisk#-getting-started'
    },
      classifiers=[
	    	"Programming Language :: Python :: 3.6",
	    	"License :: OSI Approved :: MIT License",
	    	"Operating System :: OS Independent",
	    ],
      include_package_data=True,
      )
