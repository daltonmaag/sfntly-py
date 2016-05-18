# sfntly-py

Python bindings for Google's [sfntly](https://code.google.com/p/sfntly), a font manipulation library written in Java.

The package currently include the following modules:

#### sfntly.sfnttool

* `convert(fmt, infile, outfile="", verbose=False, save_log=False)`

    Use "sfnttool.jar" to convert the input font file 'infile' to format 'fmt'. Supported formats are EOT and WOFF 1.0.
    Return 0 if successful, else return an error code.
    If 'verbose' is True, print messages to stdout/stderr.
    If 'save_log' is True, write exception traceback to a text file.

Example:

```python
    >>> from sfntly import sfnttool
    # save WOFF in the same location of input font
    >>> sfnttool.convert('woff', 'font.ttf')
    0
    # save EOT to destination 'outfile', and print more info to stdout
    >>> sfnttool.convert('eot', 'font.ttf', outfile='webfonts/font.eot', verbose=True)
    $ java -jar sfnttool.jar -e -x "font.ttf" "webfonts/font.eot"
    Exception in thread "main" java.lang.IllegalArgumentException: source table must not be null
    [...]
    1
```

## Requirements

- Python 2.7 or above
- Java Runtime Environment 7 or above.

## Download

Pre-compiled Python wheels are available at:
<https://github.com/daltonmaag/sfntly-py/releases/latest>

## Build requirements

- Java Development Kit 7 or above
- [Apache Ant](http://ant.apache.org/):
	- OSX: available via [Homebrew](http://brew.sh/), `brew install ant`
	- Windows: you can use the [winant](https://code.google.com/p/winant/) installer

## Build instructions

    git clone --recursive https://github.com/daltonmaag/sfntly-py.git
    cd sfntly-py
    python setup.py build
    python setup.py install

Please ensure the 'ant' executable can be found in the user's PATH variable.
