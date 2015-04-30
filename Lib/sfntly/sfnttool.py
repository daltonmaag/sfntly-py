""" Use 'sfnttool' from Google sfntly to convert fonts to EOT and WOFF.
Requires Java JRE7 or above.

Usage:
sfnttool.convert('eot', '/path/to/input.ttf', outfile='/path/to/output.eot')
"""
from __future__ import print_function, absolute_import
import os
from sfntly.javaBridge import _runShell, JAVA_PATH, SFNTTOOL_PATH
from damaTools.misc.py23 import *
import sys


def convert(fmt, infile, outfile="", verbose=False, save_log=True):
    """Convert input file to either WOFF or EOT using sfnttool.jar.
    When no outfile is specified, the destination is saved in the same folder
    as infile.
    Optionally save a log file when the tool fails to convert the webfont.
    """
    if not JAVA_PATH:
        raise Exception("Java executable not found")
    if not SFNTTOOL_PATH:
        raise Exception("sfnttool.jar not found")
    fmt = fmt.lower()
    if fmt not in ['woff', 'eot']:
        raise Exception('Unknown webfont format: %s' % fmt)
    infile = tounicode(infile, encoding=sys.getfilesystemencoding())
    infile = os.path.abspath(infile)
    if outfile == "":
        outfile = os.path.splitext(infile)[0] + '.' + fmt
    else:
        outfile = tounicode(outfile, encoding=sys.getfilesystemencoding())
    outfile = os.path.abspath(outfile)
    savedir, _ = os.path.split(outfile)
    if not os.path.isfile(infile):
        raise Exception('%s is not a file!' % infile)
    if not os.path.exists(savedir):
        raise Exception('The folder "%s" does not exist!' % savedir)
    if fmt == "woff":
        cmd = '"%s" -jar "%s" -w "%s" "%s"' % (JAVA_PATH, SFNTTOOL_PATH,
                                               infile, outfile)
    elif fmt == "eot":
        cmd = '"%s" -jar "%s" -e -x "%s" "%s"' % (JAVA_PATH, SFNTTOOL_PATH,
                                                  infile, outfile)
    if verbose:
        infname = os.path.basename(infile)
        short_cmd = 'java -jar sfnttool.jar '
        if fmt == "woff":
            short_cmd += '-w "%s" "%s"' % (infile, outfile)
        elif fmt == 'eot':
            short_cmd += '-e -x "%s" "%s"' % (infile, outfile)
        print(short_cmd)
    retcode, stdout = _runShell(cmd)
    if retcode != 0:
        if verbose:
            print("%s conversion failed! Plase read the 'snfttool_log.txt'" %
                  fmt.upper())
        if os.path.exists(outfile):
            os.remove(outfile)
        if save_log:
            msg = cmd+"\n"+stdout+"\n"
            logpath = os.path.join(savedir, "snfttool_log.txt")
            logfile = open(logpath, 'a')
            logfile.write(msg)
            logfile.close()
    return retcode
