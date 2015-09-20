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

import re
from os import path
import shutil


class Kernel:

    def __init__(self, location):
        # User-expant the kernel sources location if necessary.
        self.location = path.expanduser(location)
        # Read the Makefile into memory.
        try:
            with open(path.join(self.location, 'Makefile'), 'r') as makefile:
                makefile_contents = makefile.read()
        except:
            print("Are you sure", self.location, "is a directory with kernel",
                  "sources?")
            exit(1)
        # Extract version.
        version = re.sub(r'.*VERSION\s=\s(\d*)[\s\n]+.*', r'\1',
                         makefile_contents, flags=re.DOTALL)
        # Extract patch level.
        patchlevel = re.sub(r'.*PATCHLEVEL\s=\s(\d*)[\s\n]+.*', r'\1',
                            makefile_contents, flags=re.DOTALL)
        # Extract sub level.
        sub = re.sub(r'.*SUBLEVEL\s=\s(\d*)[\s\n]+.*', r'\1',
                     makefile_contents, flags=re.DOTALL)
        # Extract extra version.
        extra = re.sub(r'.*EXTRAVERSION\s=\s([^\s\n]*)[\s\n]+.*', r'\1',
                       makefile_contents, flags=re.DOTALL)
        if version == "" or patchlevel == "" or sub == "":
            print("The kernel Makefile does not contain proper version",
                  "information.")
            exit(1)
        # Extract version name.
        name = re.sub(r'.*NAME\s=\s([^\n]*)\n+.*', r'\1',
                      makefile_contents, flags=re.DOTALL)
        print(name)
        # Build major version number.
        self.major_version = version + "." + patchlevel
        # Build full version number.
        self.full_version = version + "." + patchlevel + "." + sub + extra

    def backup_config(self, destination='.config.old'):
        # Backup current .config to .config.old just in case.
        if path.isfile(path.join(self.location, '.config')):
            shutil.copy2(path.join(self.location, '.config'),
                         path.join(self.location, destination))
