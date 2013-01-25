#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010-2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from __future__ import with_statement
__version__ = "$Revision$ $Date$"
__author__    = "Guillaume Bour <gbour@proformatique.com>"
__author__    = "Steven Le Bras <slebras@avencall.com>"

import sys
import urllib2
import httplib
import os
import os.path
from optparse import OptionParser

def main():
    gxp = GetXivoPackages()
    gxp.list_and_download_packages()


class GetXivoPackages():
    def __init__(self):
        self.SUITES    = {
            'skaro': [
                'squeeze-xivo-skaro-rc/main/binary-i386/Packages',
                'squeeze-xivo-skaro-rc/non-free/binary-i386/Packages',
                'squeeze-xivo-skaro/main/binary-i386/Packages',
                'squeeze-xivo-skaro/non-free/binary-i386/Packages',
                'squeeze/main/binary-i386/Packages',
                'squeeze/contrib/binary-i386/Packages',
                'squeeze/non-free/binary-i386/Packages',
            ],
        }
        self._parse_arguments()
        self.DAKBASE = 'http://mirror.xivo.fr/%s/dists/' % self.debian_or_archive
        self._whitelist()
        self.stats         = {'size': 0, 'installed-size': 0}
        self.packages = []

    def list_and_download_packages(self):
        self._list_packages()
        self.packages.sort()
        if self.options.list:
            self._print_list()
        self._download_packages()

    def _parse_arguments(self):
        usage    = "Usage: %prog [options] path/to/download"
        self.parser = OptionParser(usage=usage)
        self.parser.add_option('-l', '--list-packages'                 , dest='list'         , action='store_true',
            default=False, help="list available packages (do not download)")
        self.parser.add_option('-f', '--force'                 , dest='force'         , action='store_true',
            default=False, help="force re-download all packages")
        self.parser.add_option('-V', '--version'                 , dest='version'         , action='store',
            type='string', default='current', help="specify the XiVO version to build. Default is 'curent'")
        self.parser.add_option('-s', '--suite'     , dest='suite'    , action='store',
            type='string', default='skaro', help="XiVO suite. set SUITE to 'list' to list all available suites")

        (self.options, self.args) = self.parser.parse_args()
        self._validate_args()

    def _validate_args(self):
        if self.options.version in ['current']:
            self.debian_or_archive = '/debian/'
        else:
            self.debian_or_archive = '/archive/'
            self.SUITES    = {
                'skaro': [
                    'squeeze-xivo-skaro-%s/main/binary-i386/Packages' % (self.options.version),
                    'squeeze-xivo-skaro-%s/non-free/binary-i386/Packages' % (self.options.version),
                ],
            }

        if self.options.suite in ['list']:
            print "Available suites:"
            for suite in self.SUITES.keys():
                print " *", suite
            sys.exit(0)

        if not self.options.list and len(self.args) != 1:
            self.parser.print_help(); sys.exit(2)

        if self.options.suite not in self.SUITES:
            print "Unknown suite", self.options.suite; sys.exit(2)

    def _whitelist(self):
        if self.options.suite == "skaro-dev":
            self.include = [
                'pf-fai-xivo-1.2-skaro-dev',
                'pf-fai-dev',
            ]
        elif self.options.suite == "skaro-rc":
            self.include = [
                'pf-fai-xivo-1.2-skaro',
                'pf-fai',
            ]
        elif self.options.suite == "skaro":
            if self.options.version in ['current']:
                self.include = [
                    'pf-fai-xivo-1.2-skaro',
                    'pf-fai',
                ]
            else:
                self.include = [
                    'xivo-fai-skaro-%s' % (self.options.version),
                ]
        self.exclude = [
            'cracklib',
            'dahdi-linux-source',
            'libcrack2',
            'libctl',
            'libnet-ssh-ruby',
            'libruby',
            'meep', 'libmeep',
            'misdn-kernel-source',
            'mpb',
            'pf-sys-ssh',
            'pfbotnet', 'libpfbotnet',
            'python-cap',
            'python-crack',
            'sangoma-dbg',
            'sangoma-wanpipe-source',
            'squid',
            'swig',
            'tshark',
            'wireshark',
            'xivo-dev-ssh-pubkeys',
        ]
        self.skip=False

    def _list_packages(self):
        for src in self.SUITES[self.options.suite]:
            f = urllib2.urlopen(self.DAKBASE + src)
            for line in f.readlines():
                if line.startswith('Package:'):
                    self.skip = True
                    pacnam = line.split(' ')[1][:-1]

                    if not pacnam in self.include and \
                            (pacnam.endswith('-dev') or \
                            len(filter(lambda x: pacnam.startswith(x), self.exclude)) > 0):
                        continue
                    
                    self.skip = False

                if self.skip:
                    continue

                if line.startswith('Installed-Size:'):
                    self.stats['installed-size'] += int(line.split(' ')[1])
                elif line.startswith('Size:'):
                    self.stats['size'] += int(line.split(' ')[1])
                elif line.startswith('Filename:'):
                    if 'dalek' in line:
                        continue
                
                    self.packages.append(line.split(' ')[1][:-1])

            f.close()
            
    def _print_list(self):
        import pprint; pprint.pprint(self.packages)
        print self.stats
        sys.exit(0)

    def _download_packages(self):
        if not os.path.exists(self.args[0]):
            os.makedirs(self.args[0])
        
        conn = httplib.HTTPConnection('mirror.xivo.fr')
        for package in self.packages:
            debfile = package.rsplit('/', 1)[-1]
            print " . downloading", debfile, ':',

            if os.path.exists(self.args[0] + '/' + debfile):
                localsize = os.path.getsize(self.args[0] + '/' + debfile)
                
                conn.request("HEAD", self.debian_or_archive + package)
                resp = conn.getresponse()
                try:
                    netsize     = int(dict(resp.getheaders()).get('content-length'))
                except:
                    netsize     = -1
                conn.close()
                
                if netsize == localsize:
                    print 'skipping...'; continue
            
            print '...'
            conn.request("GET", self.debian_or_archive + package)
            print self.debian_or_archive + package
            resp = conn.getresponse()
            
            with open(self.args[0] + '/' + debfile, 'wb') as f:
                while True:
                    data = resp.read(8192)
                    if len(data) == 0:
                        break
                        
                    f.write(data)
                
            conn.close()

if __name__ == '__main__':
    main()
