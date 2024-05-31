from setuptools import setup, find_packages

# Define project metadata
NAME = 'PopularWinCmds'
DESCRIPTION = 'Simple commands from the CMD prompt directly in your python script'
AUTHOR = 'Sion'
AUTHOR_EMAIL = 'the.rckr@gmail.com'
VERSION = '0.1.0'


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Operating System :: MacOS',
],

)
