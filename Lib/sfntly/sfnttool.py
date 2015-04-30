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


def convert(fmt, infile, outfile="", verbose=False, save_log=False):
    """Convert input file to either WOFF or EOT using sfnttool.jar.
    When no outfile is specified, the destination is saved in the same folder
    as infile.
    If 'verbose' is True, print messages to stdout or stderr.
    Optionally 'save_log' to file when the command returns an error.
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
        cmd = u'"%s" -jar "%s" -w "%s" "%s"' % (JAVA_PATH, SFNTTOOL_PATH,
                                               infile, outfile)
    elif fmt == "eot":
        cmd = u'"%s" -jar "%s" -e -x "%s" "%s"' % (JAVA_PATH, SFNTTOOL_PATH,
                                                  infile, outfile)
    if verbose:
        short_cmd = u'$ java -jar sfnttool.jar '
        if fmt == "woff":
            short_cmd += u'-w "%s" "%s"' % (infile, outfile)
        elif fmt == 'eot':
            short_cmd += u'-e -x "%s" "%s"' % (infile, outfile)
        print(short_cmd)
    retcode, stdout = _runShell(cmd)
    if retcode != 0:
        if save_log:
            if not verbose:
                print("%s conversion failed! Plase read the 'snfttool_log.txt'" %
                      fmt.upper(), file=sys.stderr)
            from io import open
            msg = cmd+"\n"+stdout+"\n"
            logpath = os.path.join(savedir, "snfttool_log.txt")
            logfile = open(logpath, 'a', encoding='utf-8')
            logfile.write(msg)
            logfile.close()
        if verbose:
            print(stdout, file=sys.stderr)
        if os.path.exists(outfile):
            os.remove(outfile)
    return retcode
