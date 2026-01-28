**Updating to API version 3.0+ (Python 3)** - random things we've run across and definitely not exhaustive
- `print` statement change - in python 3 it requires that the string be enclosed in parens:
  ```python
  # Python 2:
  print "some string here"
  # Python 2 & 3:
  print("some string here")
  ```

- Exception declarations 

  ```python
  # Python 2:
  except ExceptionHere, exc:
  # Python 2 & 3:
  except ExceptionHere as exc:
  ```

- The **`StandardError`** exception is deprecated, so replace with **`Exception`**

- JSON

  ```python
  # In API versions < 3.0, this works:
  import simplejson
  import simplejson as json
  # In API versions >= 3.0:
  import json
  ```

- unicode is no longer a type, so this fails:

  ```python
  isinstance(some_var, unicode)
  ```

  since all strings are by default unicode

- replace **`file()`** with **`open()`**

- if opening a utf-8 file, **`open("file.json", encoding="utf-8")`**

- **`indigo.kStateImageSel.None`** is now a syntax error because None is a keyword. You must change those occurrances to **`indigo.kStateImageSel.NoImage`** in Python 3. Also, you can use the following in place of the indigo specifier directly and it should work correctly in either version:

  ```python
  getattr(indigo.kStateImageSel, "NoImage", getattr(indigo.kStateImageSel, "None", ""))
  ```

  which could also be written as a function:

  ```python
  def _no_image():
      try:
          return getattr(indigo.kStateImageSel, "NoImage")
      except:
          return getattr(indigo.kStateImageSel, "None")
  ```

- **`socket.error`** is aliased to `OSError` (and it's deprecated anyway), though **`socket.timeout`** remains. There is now a top-level exception called **`ConnectionResetError`** which may be what you were looking for: also **`ConnectionRefusedError`**. Just don't get fooled if you try to subscript what you think is a `socket.error` only to get a message about OSError not being subscriptable...

- **socket** communication now uses the `bytes` data type rather than `str` (because `str` is now unicode). If your plugin uses socket communications, you are going to need to make sure that you encode/decode appropriately in the code that surrounds your socket communication. If you have a string (like json for instance), then you'll need to encode that `str` into `bytes`. Likewise, when you receive something from a socket you'll need to decode those `bytes` into a `str`. Simple example:

  ```python
  >>> s = "Testing special characters like é, ç, etc"
  >>> b = s.encode("utf8")
  >>> b
  b'Testing special characters like \xc3\xa9, \xc3\xa7, etc'
  >>> b.decode("utf8")
  'Testing special characters like é, ç, etc'
  ```

  Don't forget to convert when using for logging messages where you insert them using the format() command or you'll end up seeing some strangeness:

  ```python
  >>> "bytes: {}".format(b)
  "bytes: b'Testing special characters like \\xc3\\xa9, \\xc3\\xa7, etc'"
  >>> "str: {}".format(b.decode("utf8"))
  'str: Testing special characters like é, ç, etc'
  ```

- Division results on integers can result in a float: 

  ```python
  >>> # python 2
  ... 2/3
  0
  >>> # python 3
  >>> 2/3
  0.6666666666666666
  ```

  but you can get old results by using double slashes:

  ```python
  >>> # python 3
  >>> 2//3
  0
  ```

  which, btw, also works in python 2.7

- Many `dict` iterators (`items()`, `keys()`, `values()`) now return "view" objects. In general this isn't an issue, but if you are deleting stuff while iterating through one of those views, you'll get a RuntimeError:

  ```python
  d = {"a": 1, "b": 2, "c": 3}
  for k in d.keys():
      del d[k]
      
  Traceback (most recent call last):
    File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/code.py", line 90, in runcode
      exec(code, self.locals)
    File "<input>", line 1, in <module>
  RuntimeError: dictionary changed size during iteration
  
  ```

  so you'll first want to make a copy to iterate over:

  ```python
  for k in d.copy().keys():
      del d[k]
  ```

- `dict.iteritems()` is deprecated, `dict.items()` works just as well in both python 2 & 3 (same for all the iter* functions on dict and list objects).

- `pylint -py3k` may give you this error: `round built-in referenced (round-builtin)`. This warning can safely be ignored since it's primarily just a reminder that the [algorithm for calculating how an exact halfway cases](https://docs.python.org/3/whatsnew/3.0.html#builtins) has changed in python 3.
