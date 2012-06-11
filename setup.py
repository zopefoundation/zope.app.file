##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.app.file package

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.app.file',
      version='3.6.1',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='File and Image -- Zope 3 Content Components',
      long_description=(
          read('README.txt')
          + '\n\n.. contents::\n\n' +
          read('src', 'zope', 'app', 'file', 'browser', 'file.txt')
          + '\n\n' +
          read('src', 'zope', 'app', 'file', 'browser', 'url.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope3 file image content",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/zope.app.file',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      extras_require = dict(test=['zope.app.testing',
                                  'zope.app.securitypolicy',
                                  'zope.app.zcmlfiles',
                                  'zope.publisher >= 3.12',
                                  'zope.login',
                                  ]),
      install_requires=['setuptools',
                        'transaction',
                        'ZODB3',
                        'zope.app.publication',
                        'zope.contenttype>=3.5.0dev',
                        'zope.datetime',
                        'zope.dublincore>=3.7',
                        'zope.event',
                        'zope.exceptions',
                        'zope.filerepresentation',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.schema',
                        'zope.site',
                        'zope.size',
                        ],
      include_package_data = True,
      zip_safe = False,
      )
