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
from docutils.core import publish_file
import glob
import os
import setuptools
import sys

version='0.1.5'

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
if '--user' in sys.argv or not os.access('/etc', os.R_OK | os.W_OK | os.X_OK):
    etc_dir = '../.config'
else:
    etc_dir = '/etc'
etc_dir = os.path.join(etc_dir, 'kernelconfig')

setuptools.setup(
    name='kernelconfig',
    version=version,
    description="""
        Generate custom Linux kernel configurations from curated sources
        """,
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
    install_requires=['beautifulsoup4', 'lxml'],
    data_files=[('share/kernelconfig', glob.glob('sources/*')),
                (etc_dir, glob.glob('settings/*')),
                ('share/doc/kernelconfig-' + version, ['README.html'])],
    entry_points={'console_scripts': ['kernelconfig=kernelconfig.main:run']})
