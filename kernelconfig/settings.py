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

import configparser
from os import path
import re
import subprocess
import tempfile


class Settings:

    def __init__(self, settings, kernel):
        self._settings = configparser.ConfigParser(allow_no_value=True,
                                                   delimiters='|',
                                                   comment_prefixes="#")
        # User-expand the path if necessary and check if it's an absolute path.
        if path.isabs(path.expanduser(settings)):
            # It is, so let's use that.
            settings_file = settings
        else:
            # It's not an absolute path, so let's try and figure out what it is
            # relative to.
            for search_dir in ['~/.config', '/etc']:
                try_file = path.join(search_dir, 'kernelconfig', settings)
                if path.isfile(path.expanduser(try_file)):
                    settings_file = path.expanduser(try_file)
                    break
            else:
                # Couldn't find anything.
                settings_file = ''
        # Does the target file actually exist?
        if not path.isfile(settings_file):
            raise OSError("settings file not found (" + settings + ")")
        # File exists, we're go. Inform the user.
        print("Using settings in " + settings_file)
        # Read the settings file.
        self._settings.read(settings_file)
        # Set the path to the .config file in the kernel sources directory.
        self._config_path = path.join(kernel, '.config')

    def setup_base(self, arch, version):
        here = path.abspath(path.dirname(__file__))
        # Create a temporary directory for the source script to work in.
        with tempfile.TemporaryDirectory(prefix='kernelconfig.') as tmpdir:
            # We currently only support one source at the same time, so let's
            # extract the first line in the [source] section of the settings
            # file.
            base = self._settings['source'].popitem()[0]
            # There may be arguments on that line for the source script, so
            # let's split it all.
            base_cmd = base.split(' ')
            # The actual command is the first item, prefix it with the path to
            # get at it.
            # TODO allow path to an arbitrary file
            base_cmd[0] = path.join(here,
                                    '../../../../share/kernelconfig/sources',
                                    base_cmd[0])
            # Insert the desired architecture and version as the first and
            # second mandatory arguments.
            base_cmd[1:1] = [self._config_path, arch, version]
            # Call the source script and add the original arguments if any at
            # the end.
            subprocess.check_call(base_cmd, cwd=tmpdir)

    def process_options(self):
        # Read the .config in the kernel sources directory into memory, so that
        # we don't have to open and close the file multiple times.
        with open(self._config_path, 'r') as config_file:
            self._config = config_file.read()
        # Deal with each line in the [options] section of the settings file.
        for option in self._settings['options']:
            # Split all words on the line, the first one is the action.
            option_list = option.split(' ')
            # The action must be among these:
            dispatcher = {
                'enable': self._enable,
                'disable': self._disable,
                'module': self._module,
                'set': self._set}
            action = dispatcher.get(option_list[0])
            # Execute the action onto however many options there were on this
            # line.
            action(option_list[1:])
        with open(self._config_path, 'w') as config_file:
            config_file.write(self._config)

    def _enable(self, option_list):
        # There can be multiple options to enable on the same line.
        for option in option_list:
            print("Enabling " + option.upper())
            # Delete any occurence of this option in the current .config file.
            self._delete_option(option.upper())
            # Add enabled option at the end of the .config file.
            self._config = self._config + "CONFIG_" + option.upper() + "=y\n"

    def _disable(self, option_list):
        # There can be multiple options to disable on the same line.
        for option in option_list:
            print("Disabling " + option.upper())
            # Delete any occurence of this option in the current .config file.
            self._delete_option(option.upper())
            # Add disabled option at the end of the .config file.
            self._config = self._config + "# CONFIG_" + option.upper() + \
                " is not set\n"

    def _module(self, option_list):
        # There can be multiple options to set as module on the same line.
        for option in option_list:
            print("Setting " + option.upper() + " as module")
            # Delete any occurence of this option in the current .config file.
            self._delete_option(option.upper())
            # Add option as module at the end of the .config file.
            self._config = self._config + "CONFIG_" + option.upper() + "=m\n"

    def _set(self, option_list):
        # There can be multiple options to set to a value on the same line.
        for option in option_list:
            option = option.split('=')[0].upper() + "=" + option.split('=')[1]
            print("Setting " + option)
            # Delete any occurence of this option in the current .config file.
            self._delete_option(option.split('=')[0].upper())
            # Add option set to value at the end of the .config file.
            self._config = self._config + "CONFIG_" + option + "\n"

    def _delete_option(self, option):
        # The entire .config file is treated as one giant string. Thus, locate
        # the fragment which corresponds to the line with the option we want to
        # delete and only keep what is before and after.
        self._config = re.sub(r'(.*\n)[^\n]*CONFIG_' + option +
                              r'[ =][^\n]*\n(.*)', r'\1\2', self._config)
