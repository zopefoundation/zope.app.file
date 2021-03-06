Special URL handling for DTML pages
===================================

When an HTML File page containing a head tag is visited, without a
trailing slash, the base href isn't set.  When visited with a slash,
it is:


  >>> print(http(r"""
  ... POST /+/zope.app.file.File%3D HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Length: 610
  ... Content-Type: multipart/form-data; boundary=---------------------------32826232819858510771857533856
  ... Referer: http://localhost:8081/+/zope.app.file.File=
  ...
  ... -----------------------------32826232819858510771857533856
  ... Content-Disposition: form-data; name="field.contentType"
  ...
  ... text/html
  ... -----------------------------32826232819858510771857533856
  ... Content-Disposition: form-data; name="field.data"; filename=""
  ... Content-Type: application/octet-stream
  ...
  ...
  ... -----------------------------32826232819858510771857533856
  ... Content-Disposition: form-data; name="UPDATE_SUBMIT"
  ...
  ... Add
  ... -----------------------------32826232819858510771857533856
  ... Content-Disposition: form-data; name="add_input_name"
  ...
  ... file.html
  ... -----------------------------32826232819858510771857533856--
  ... """))
  HTTP/1.1 303 See Other
  ...

  >>> print(http(r"""
  ... POST /file.html/edit.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Content-Length: 507
  ... Content-Type: multipart/form-data; boundary=---------------------------10196264131256436092131136054
  ... Referer: http://localhost:8081/file.html/edit.html
  ...
  ... -----------------------------10196264131256436092131136054
  ... Content-Disposition: form-data; name="field.contentType"
  ...
  ... text/html
  ... -----------------------------10196264131256436092131136054
  ... Content-Disposition: form-data; name="field.data"
  ...
  ... <html>
  ... <head></head>
  ... <body>
  ... <a href="eek.html">Eek</a>
  ... </body>
  ... </html>
  ... -----------------------------10196264131256436092131136054
  ... Content-Disposition: form-data; name="UPDATE_SUBMIT"
  ...
  ... Change
  ... -----------------------------10196264131256436092131136054--
  ... """))
  HTTP/1.1 200 Ok
  ...

  >>> print(http(r"""
  ... GET /file.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """))
  HTTP/1.1 200 Ok
  ...
  <html>
  <head></head>
  <body>
  <a href="eek.html">Eek</a>
  </body>
  </html>


  >>> print(http(r"""
  ... GET /file.html/ HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... """))
  HTTP/1.1 200 Ok
  ...
  <html>
  <head>
  <base href="http://localhost/file.html" />
  </head>
  <body>
  <a href="eek.html">Eek</a>
  </body>
  </html>
