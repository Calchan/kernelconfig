==============
 kernelconfig
==============

Generate custom Linux kernel configurations from curated sources.

(Note. kernelconfig is a port to python of a previously privately-only released
tool called genconfig. The latter, before it died a horrible death at 5400rpm
or so, had much more advanced features than kernelconfig has right now, but
these will be re-introduced progressively. Error handling is currently mostly
taken care of by python, so, although it won't send you off track, error
messages may look a bit cryptic at times. This too will be improved.
kernelconfig is however released now since, even in its current state, it is
very functional and equally useful.)


Introduction
============

TL;DR kernelconfig will automatically download a base configuration matching
the kernel you want to compile from a curated source of your choice (Debian,
Ubuntu, Fedora, Liquorix, etc...), customize it with a number of options which
suit your taste and needs, and much more.

You can do that, for example::

    $ kernelconfig -k /usr/src/linux-4.2

and it will automatically generate the .config file for you. No questions
asked.

Or that::

    $ kernelconfig -k /usr/src/linux-4.2 -v 4.1

in case the curated source in your settings does not have a base configuration
for kernel version 4.2 but has one for version 4.1. Expect to have to answer
some questions if/when you run 'make oldconfig' before compiling your kernel.

Or, still::

    $ kernelconfig -k /usr/src/linux-4.2 --arch arm

if you are going to cross-compile a kernel for arm.

Here is a simple example of a settings file::

    [source]
    ubuntu --lowlatency

    [options]
    disable MODULE_SIG
    enable BLK_DEV_SD SATA_AHCI
    enable BTRFS_FS
    module EVBUG

This will automatically download a version-matching Ubuntu configuration with
low-latency options, disable verification of module signatures, build the SCSI
disk and SATA AHCI drivers into the kernel (i.e., not as modules) to be able to
boot without an initramfs, and also build the BTRFS driver into the kernel for
the same reason. Finally, we make sure EVBUG is compiled as a module to only
load it when necessary since it will pollute the system log. This will be done
consistently and automatically every time you will need to compile a new
kernel. All that with the comfort of a whole team of upstream developers
handling the grunt work for you. As Tom and Ray Magliozzi like(d) to say:
"Pretty cute, huh?"

If you are the kind of perverted individual who likes reading manuals, then
read on. If not, get used to being mocked.


Installing kernelconfig
=======================

The best way is, if possible, to rely on you distribution's package manager.

Alternatively you can install it from PyPI using pip. For example, as root:

    $ pip3 install kernelconfig

The default settings file and examples will be installed into
'/etc/kernelconfig'.

Whether root or not, it is possible to make a user installation, like this:

    $ pip3 install --user kernelconfig

In this case, the default settings file and examples will be installed into
'~/.config/kernelconfig'.


Optional arguments
==================

 * -h, --help

   Show the help message and exit.

 * -a ARCH, --arch ARCH

   Force the kernel configuration architecture. ARCH is as returned by 'uname
   -m'. Useful for cross-compiling.

 * -k KERNEL, --kernel KERNEL

   Path to the unpacked kernel sources directory. It can be absolute or
   relative to the current working directory. The default is '.', the current
   working directory.

 * -s SETTINGS, --settings SETTINGS

   Path to the settings file. It can be an absolute or user-expandable path to
   an arbitrary file. If it is a relative path, then the file will be searched
   for relatively to ~/.config/kernelconfig first and then /etc/kernelconfig.
   Sub-directories relative to both these locations can be used. If a path
   relative to the current working directory is desired, prefix it with './'.
   The default is 'default', i.e., '~/.config/kernelconfig/default' if it
   exists, or, failing that, '/etc/kernelconfig/default'.

 * -v VERSION, --version VERSION

   Force the kernel configuration version. Useful when there is no matching
   major kernel version in the curated source.


Settings syntax
===============

A comment line starts with a '#' as its first character.

Lines can be empty. There is no limit as to how many consecutive empty lines
there can be.


[source] section
----------------

Lines other than the first non-empty and non-comment line will be discarded.

A source is the name of an executable in either '/usr/share/kernelconfig' or
'~/.local/share/kernelconfig', depending on the instalation being of the --user
type or not, possibly followed by a number of optional arguments. For example::

    liquorix --pae

or::

    ubuntu --lowlatency

See "Curated sources" below for a list of supported sources and optional
arguments.


[options] section
-----------------

A list of one action per line followed by one or more kernel options to perform
the action on. No indentation is allowed, but empty and comment lines are
possible.

Actions:

 * **enable**: enable the option in the kernel, not as module.
   For example::

       enable BLK_SD_DEV SATA_AHCI

   Build the BLK_SD_DEV and ATA_AHCI drivers into the kernel so that it is
   bootable without the need for an initramfs.
 
 * **module**: enable the option as module only so as to be able to only load
   it when desired. For example::

       module EVBUG

   The EVBUG driver is available to load for debugging when necessary.

 * **disable**: disable the option entirely. For example::

       disable MODULE_SIG

   Disable module signature verification.

 * **set**: set an option to a given value. For example::

       set DEFAULT_IOSCHED="bfq"

   Use Budget Fair Queueing as the default I/O scheduler.

Note 1. Do no prefix options names with 'CONFIG\_'. kernelconfig takes care of
that for you.

Note 2. Option names will always be capitalized for you if you don't. It is
however easier to read a settings file whose options are capitalized.


Curated sources
===============

Here is a list of the currently supported curated sources. More will come.


Liquorix
--------

 * Name in settings: liquorix
 
 * Supported architectures: i386, i686, x86_64
 
 * Options:

   * --pae: enable Physical Address Extension on processors supporting it to
     extend physical address space 4GB (i386 and i686 only).


Ubuntu
------

  * Name in settings: ubuntu

  * Supported architectures: i386, i686, x86_64 (upstream supports more, will
    come later)

  * Options:

    * --lowlatency: enable low-latency timing and preemption options.
