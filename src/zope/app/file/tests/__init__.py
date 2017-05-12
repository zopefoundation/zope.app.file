#
# This file is necessary to make this directory a package.

from zope.app.wsgi.testlayer import http as _http
from zope.app.file.testing import AppFileLayer

def http(query_str, *args, **kwargs):
    wsgi_app = AppFileLayer.make_wsgi_app()
    # Strip leading \n
    query_str = query_str.lstrip()
    kwargs.setdefault('handle_errors', False)
    if not isinstance(query_str, bytes):
        query_str = query_str.encode("utf-8")
    return _http(wsgi_app, query_str, *args, **kwargs)
