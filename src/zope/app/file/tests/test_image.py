##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Test Image content component

"""
import unittest
from zope.interface.verify import verifyClass
from zope.app.file.interfaces import IImage
from zope.app.file.image import Image, FileFactory, ImageSized
from zope.app.file.file import File, FileWriteFile, FileReadFile

zptlogo = (
    b'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
    b'\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
    b'\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
    b'\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
    b'\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
    b'\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
    b'\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
    b'\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
    b'\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
    b'\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04'
    b'\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4'
    b'\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
    b'\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
    b'\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
    b'\x00A\x00;'
    )

class TestImage(unittest.TestCase):

    def _makeImage(self, *args, **kw):
        return Image(*args, **kw)

    def testEmpty(self):
        file = self._makeImage()
        self.assertEqual(file.contentType, '')
        self.assertEqual(file.data, b'')

    def testConstructor(self):
        file = self._makeImage(b'Data')
        self.assertEqual(file.contentType, '')
        self.assertEqual(file.data, b'Data')

    def testMutators(self):
        image = self._makeImage()

        image.contentType = 'image/jpeg'
        self.assertEqual(image.contentType, 'image/jpeg')

        image._setData(zptlogo)
        self.assertEqual(image.data, zptlogo)
        self.assertEqual(image.contentType, 'image/gif')
        self.assertEqual(image.getImageSize(), (16, 16))

    def testInterface(self):
        self.assertTrue(IImage.implementedBy(Image))
        self.assertTrue(verifyClass(IImage, Image))

class TestFileAdapters(unittest.TestCase):

    def _makeFile(self, *args, **kw):
        return Image(*args, **kw)

    def test_ReadFile(self):
        file = self._makeFile()
        content = b"This is some file\ncontent."
        file.data = content
        file.contentType = 'text/plain'
        self.assertEqual(FileReadFile(file).read(), content)
        self.assertEqual(FileReadFile(file).size(), len(content))

    def test_WriteFile(self):
        file = self._makeFile()
        content = b"This is some file\ncontent."
        FileWriteFile(file).write(content)
        self.assertEqual(file.data, content)

class DummyImage(object):

    def __init__(self, width, height, bytes):
        self.width = width
        self.height = height
        self.bytes = bytes

    def getSize(self):
        return self.bytes

    def getImageSize(self):
        return self.width, self.height


class TestFileFactory(unittest.TestCase):

    def test_image(self):
        factory = FileFactory(None)
        f = factory("spam.txt", "image/foo", b"hello world")
        self.assertIsInstance(f, Image)
        f = factory("spam.txt", "", zptlogo)
        self.assertIsInstance(f, Image)

    def test_text(self):
        factory = FileFactory(None)
        f = factory("spam.txt", "", b"hello world")
        self.assertIsInstance(f, File)
        self.assertNotIsInstance(f, Image)
        f = factory("spam.txt", "", b"\0\1\2\3\4")
        self.assert_(isinstance(f, File), f)
        self.assertIsInstance(f, File)
        self.assertNotIsInstance(f, Image)
        f = factory("spam.txt", "text/splat", zptlogo)
        self.assertIsInstance(f, File)
        self.assertNotIsInstance(f, Image)
        f = factory("spam.txt", "application/splat", zptlogo)
        self.assertIsInstance(f, File)
        self.assertNotIsInstance(f, Image)


class TestSized(unittest.TestCase):

    def testInterface(self):
        from zope.size.interfaces import ISized
        self.assertTrue(ISized.implementedBy(ImageSized))
        self.assertTrue(verifyClass(ISized, ImageSized))

    def test_zeroSized(self):
        s = ImageSized(DummyImage(0, 0, 0))
        self.assertEqual(s.sizeForSorting(), ('byte', 0))
        self.assertEqual(s.sizeForDisplay(), u'0 KB ${width}x${height}')
        self.assertEqual(s.sizeForDisplay().mapping['width'], '0')
        self.assertEqual(s.sizeForDisplay().mapping['height'], '0')

    def test_arbitrarySize(self):
        s = ImageSized(DummyImage(34, 56, 78))
        self.assertEqual(s.sizeForSorting(), ('byte', 78))
        self.assertEqual(s.sizeForDisplay(), u'1 KB ${width}x${height}')
        self.assertEqual(s.sizeForDisplay().mapping['width'], '34')
        self.assertEqual(s.sizeForDisplay().mapping['height'], '56')

    def test_unknownSize(self):
        s = ImageSized(DummyImage(-1, -1, 23))
        self.assertEqual(s.sizeForSorting(), ('byte', 23))
        self.assertEqual(s.sizeForDisplay(), u'1 KB ${width}x${height}')
        self.assertEqual(s.sizeForDisplay().mapping['width'], '?')
        self.assertEqual(s.sizeForDisplay().mapping['height'], '?')

    def test_getImageInfo(self):
        from zope.app.file.image import getImageInfo
        getImageInfo(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C")

    def test_getImageInfo_bmp(self):
        from zope.app.file.image import getImageInfo
        t, w, h = getImageInfo(b'BMl\x05\x00\x00\x00\x00\x00\x006\x04\x00\x00('
                               b'\x00\x00\x00\x10\x00\x00\x00\x10\x00\x00\x00'
                               b'\x01\x00\x08\x00\x01\x00\x00\x006\x01\x00\x00'
                               b'\x12\x0b\x00\x00\x12\x0b\x00\x00\x00\x01\x00'
                               b'... and so on ...')
        self.assertEqual(t, "image/x-ms-bmp")
        self.assertEqual(w, 16)
        self.assertEqual(h, 16)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
