# sfntly-py

Python bindings for Google's [sfntly](https://code.google.com/p/sfntly) font manipulation library (Java).

## Modules

### sfntly.sfnttool

* `convert`: call "sfnttool.jar" to convert the input font file to EOT or WOFF 1.0 formats. Return 0 if successful, else return error code and save traceback to log file.

Example:

```python
    >>> from sfntly import sfnttool
    # save WOFF in the same location of input font
    >>> sfnttool.convert('woff', 'font.ttf')
    0
    # save EOT to destination 'outfile', and print more info to stdout
    >>> sfnttool.convert('eot', 'font.ttf', outfile='webfonts/font.eot', verbose=True)
    java -jar sfnttool.jar -e -x "font.ttf" "webfonts/font.eot"
    EOT conversion failed! Plase read the 'snfttool_log.txt'
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

Please ensure the 'ant' executable can be found in the user's PATH variable.
