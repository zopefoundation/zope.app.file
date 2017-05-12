##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Tests for zope.app.file.browser.file.

"""
import re
from zope.testing import renormalizing

from zope.component.testing import setUp, tearDown
import doctest
import unittest


def test_suite():
    checker = renormalizing.RENormalizing((
        (re.compile(r"u'(.*)'"), r"'\1'"),
    ))
    return doctest.DocTestSuite(
        "zope.app.file.browser.file",
        setUp=setUp,
        tearDown=tearDown,
        checker=checker,
    optionflags=(doctest.ELLIPSIS
                 | doctest.NORMALIZE_WHITESPACE
                 | renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2))

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")
