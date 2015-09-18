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

import argparse
import os


def run():

    from kernelconfig import settings
    from kernelconfig import kernel

    argparser = argparse.ArgumentParser(description="""
        Generate custom kernel configurations from known curated sources.
        """)
    argparser.add_argument("-a", "--arch", type=str, help="""
        Force the kernel configuration architecture. ARCH is as returned by
        'uname -m'. Useful for cross-compiling.
        """)
    argparser.add_argument("-k", "--kernel", type=str, default='.', help="""
        Path to the unpacked kernel sources directory. It can be absolute or
        relative to the current working directory. The default is '.', the
        current working directory.
        """)
    argparser.add_argument("-s", "--settings", type=str,
                           default='default',
                           help="""
        Path to the settings file. It can be an absolute or user-expandable
        path to an arbitrary file. If it is a relative path, then the file will
        be searched for relatively to ~/.config/kernelconfig first and then
        /etc/kernelconfig. Sub-directories relative to both these locations can
        be used. If a path relative to the current working directory is desired
        prefix it with './'. The default is 'default', i.e.,
        '~/.config/kernelconfig/default' if it exists, or, failing that,
        '/etc/kernelconfig/default'.
        """)
    argparser.add_argument("-v", "--version", type=str, help="""
        Force the kernel configuration version. Useful when there is no
        matching major kernel version in the curated source.
        """)
    args = argparser.parse_args()

    kernel_path = os.path.abspath(os.path.expanduser(args.kernel))
    kernel = kernel.Kernel(kernel_path)
    settings = settings.Settings(args.settings, kernel_path)

    kernel.backup_config()

    config_version = args.version or kernel.major_version
    config_arch = args.arch or os.uname()[4]

    settings.setup_base(config_arch, config_version)
    settings.process_options()
