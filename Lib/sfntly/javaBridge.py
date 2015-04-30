""" This module is the bridge between Python and the sfntly Java tools.
It uses subprocess.Popen to create a process that executes a Java program.
"""
from __future__ import print_function
import os
import sys
import subprocess
import shlex
import traceback
from pkg_resources import resource_filename
from damaTools.misc.py23 import *


# The module expects 'sfnttool.jar' to be inside 'sfntly-java-dist' sub-folder.
SFNTTOOL_PATH = resource_filename('sfntly', 'sfntly-java-dist/sfnttool.jar')
if not os.path.isfile(SFNTTOOL_PATH):
    SFNTTOOL_PATH = None


def _runShell(cmd):
    """Run a shell cmd and return a tuple with its return code and output"""
    import locale
    try:
        cmd = tostr(cmd, encoding=locale.getpreferredencoding())
    except UnicodeEncodeError as e:
        print("Error executing command: %s" % repr(cmd), file=sys.stderr)
        traceback.print_exc(1, file=sys.stderr)
        return (1, "")
    try:
        p = subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = p.communicate()[0].decode('utf-8')
        retcode = p.wait()
        if stdout and stdout[-1:] == '\n':
            # remove trailing newline character
            stdout = stdout[:-1]
        return retcode, stdout
    except:
        print("Error executing command: %s" % repr(cmd), file=sys.stderr)
        traceback.print_exc(1, file=sys.stderr)
        return (1, "")


def _mac_find_java_path():
    """ Use built-in 'java_home' command to find the path to the current Java
    version as specified in OSX Java preferences. Return full path to the java
    executable.
    """
    retcode, java_home = _runShell('/usr/libexec/java_home')
    if retcode != 0 or not java_home:
        return
    return java_home + "/bin/java"


def _win_find_java_path():
    """ Browse the Windows registry to get the path to the current JavaHome.
    Return the full path to the 'java.exe' executable.
    """
    try:
        from _winreg import OpenKey, EnumValue, QueryInfoKey, HKEY_LOCAL_MACHINE,\
            KEY_READ, KEY_WOW64_64KEY, KEY_WOW64_32KEY
    except ImportError:
        from winreg import OpenKey, EnumValue, QueryInfoKey, HKEY_LOCAL_MACHINE,\
            KEY_READ, KEY_WOW64_64KEY, KEY_WOW64_32KEY

    def _get_reg_values(path, root=HKEY_LOCAL_MACHINE):
        """ Return {value_name, value_data} dict for the registry key located
        at 'path'. First try to lookup the key in the 64-bit registry view,
        otherwise look it up in the 32-bit registry view.
        The 'root' argument can be an already open key, or any one of the pre-
        defined HKEY_* constants (default is HKEY_LOCAL_MACHINE).
        """
        try:
            k = OpenKey(root, path, 0, KEY_READ | KEY_WOW64_64KEY)
        except WindowsError:
            try:
                k = OpenKey(root, path, 0, KEY_READ | KEY_WOW64_32KEY)
            except WindowsError:
                return
        return dict([EnumValue(k, i)[:2] for i in range(QueryInfoKey(k)[1])])

    jre_path = "SOFTWARE\\JavaSoft\\Java Runtime Environment"
    jre_values = _get_reg_values(jre_path)
    if not jre_values:
        return
    java_version = jre_values['CurrentVersion']
    java_current_values = _get_reg_values(jre_path + "\\" + java_version)
    java_home = java_current_values['JavaHome']
    return java_home + "\\bin\\java.exe"


if sys.platform.startswith('win'):
    JAVA_PATH = _win_find_java_path()
elif sys.platform == 'darwin':
    JAVA_PATH = _mac_find_java_path()
else:
    JAVA_PATH = _runShell('which java')[1]
