#  kernelconfig - Generate custom kernel configurations from curated sources
#  Copyright (C) 2015 Denis Dupeyron <calchan@gentoo.org>
#
#  This program is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License version 3, as published by the
#  Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
#  SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  this program. If not, see <http://www.gnu.org/licenses/>.

import codecs
import glob
import importlib
import os
import setuptools
import sys


version = '0.3.4'


# Automatically installing python packages with system dependencies can be
# tricky on some binary distributions, so we ask the user to install them using
# their distribution's package manager.
missing_packages = []
for package in ['bs4', 'docutils', 'lxml']:
    if not importlib.find_loader(package):
        missing_packages.append(package)
if missing_packages:
    print("The following python packages cannot be found on your system, it is",
          "recommended to install them using your distribution's package",
          "manager:")
    for package in missing_packages:
        print(package)
    sys.exit(1)

# We can now import docutils
from docutils.core import publish_file

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Generate README.html from README.rst
with open('README.rst', 'r') as readme_rst, open('README.html', 'w') as \
        readme_html:
    publish_file(source=readme_rst, destination=readme_html, writer_name='html')

# If the user requested a --user install from pip or does not have read, write
# and execute access to /etc, then we install settings into
# ~/.config/kernelconfig instead instead of /etc/kernelconfig.
if '--user' in sys.argv:
    etc_dir = '../.config'
else:
    etc_dir = '/etc'
etc_dir = os.path.join(etc_dir, 'kernelconfig')

# The actual setuptools information
setuptools.setup(
    name='kernelconfig',
    version=version,
    description="""Generate custom Linux kernel configurations from curated sources""",
    long_description=long_description,
    url="https://github.com/Calchan/kernelconfig",
    author='Denis Dupeyron',
    author_email='calchan@gentoo.org',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Operating System Kernels :: Linux'],
    keywords='Linux kernel configuration',
    packages=setuptools.find_packages(),
    data_files=[('share/kernelconfig/sources', glob.glob('sources/*')),
                (etc_dir, glob.glob('settings/*')),
                ('share/doc/kernelconfig-' + version, ['README.html'])],
    entry_points={'console_scripts': ['kernelconfig=kernelconfig.main:run']})
