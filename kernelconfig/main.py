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
        Force kernel configuration architecture (useful for cross-compiling).
        """)
    argparser.add_argument("-k", "--kernel", type=str, default='.', help="""
        Path to unpacked kernel source directory (default: '.').
        """)
    argparser.add_argument("-s", "--settings", type=str,
                           default='default',
                           help="""
        Path to Settings file (relative or absolute, see documentation, default:
        'default').
        """)
    argparser.add_argument("-v", "--version", type=str, help="""
        Force kernel configuration version (useful when there is no matching
        major kernel version in the curated source).
        """)
    args = argparser.parse_args()

    kernel = kernel.Kernel(args.kernel)
    settings = settings.Settings(args.settings, args.kernel)

    kernel.backup_config()

    config_version = args.version or kernel.major_version
    config_arch = args.arch or os.uname()[4]

    settings.setup_base(config_arch, config_version)
    settings.process_options()
