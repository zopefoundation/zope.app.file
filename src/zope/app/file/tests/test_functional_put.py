##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Test HTTP PUT verb

"""

import unittest

from zope.app.file.tests import http
from zope.app.file.testing import AppFileLayer

class TestPUT(unittest.TestCase):

    layer = AppFileLayer

    def test_put(self):
        # PUT something for the first time
        response = http(r"""PUT /testfile.txt HTTP/1.1
Authorization: Basic globalmgr:globalmgrpw
Content-Length: 20
Content-Type: text/plain

This is just a test.""")

        self.assertEquals(response.getStatus(), 201)
        self.assertEquals(response.getHeader("Location"),
                          "http://localhost/testfile.txt")

        response = http(r"""GET /testfile.txt HTTP/1.1
Authorization: Basic globalmgr:globalmgrpw""")
        self.assertEquals(response.getBody(), b"This is just a test.")

        # now modify it
        response = http(r"""PUT /testfile.txt HTTP/1.1
Authorization: Basic globalmgr:globalmgrpw
Content-Length: 23
Content-Type: text/plain

And now it is modified.""")
        self.assertEquals(response.getStatus(), 200)
        self.assertEquals(response.getBody(), b"")

        response = http(r"""GET /testfile.txt HTTP/1.1
Authorization: Basic globalmgr:globalmgrpw""")
        self.assertEquals(response.getBody(), b"And now it is modified.")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
