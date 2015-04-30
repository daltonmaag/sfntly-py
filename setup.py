#!/usr/bin/env python

from setuptools import setup, Command
from distutils.command.build import build
from distutils.command.clean import clean
from setuptools.command.install import install
from distutils import log
import subprocess
import os
import shutil


# absolute path to setup.py's directory
__dirname__ = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
# sfntly lava source directory
java_src_dir = os.path.join(
    __dirname__, "vendor", "sfntly", "java")
# path to 'sfnttool.jar' after compiling from sources
sfnttool_jar = os.path.join(
    java_src_dir, "dist", "tools", "sfnttool", "sfnttool.jar")
# destination folder inside Python package
sfnttool_dest = os.path.join(
    __dirname__, "Lib", "sfntly", "sfntly-java-dist")
# compiled *.jar files that will be copied to destination
jar_files = ['sfnttool.jar']


class CleanJarCommand(clean):
    """Add '--jar' option to 'clean' command to remove compiled *.jar files."""

    user_options = clean.user_options + [
            ('jar', None, "remove all compiled *.jar files")]

    boolean_options = clean.boolean_options + ['jar']

    def initialize_options(self):
        clean.initialize_options(self)
        self.jar = None

    def run(self):
        clean.run(self)
        if self.jar or self.all:
            log.log(log.INFO, "running `ant clean` under 'vendor/sfntly/java'...")
            subprocess.call('ant clean', shell=True, cwd=java_src_dir)

            log.log(log.INFO, "removing *.jar files under 'Lib/sfntly/sfntly-java-dist'")
            for root, dirs, files in os.walk(sfnttool_dest, topdown=False):
                for name in files:
                    if os.path.splitext(name)[1].lower() == ".jar":
                        os.remove(os.path.join(root, name))


class BuildJarCommand(Command):
    """ Add 'build_jar' command to build sfntly *.jar files using 'ant', and
    copy them to destination inside the Python package.
    """

    description = "Build sfntly Java sources"

    user_options = []

    def initialize_options(self):
        pass

    def run(self):
        log.log(log.INFO, "running `ant clean dist` to compile sfntly...")
        subprocess.call('ant', shell=True, cwd=java_src_dir)
        if os.path.exists(sfnttool_jar):
            shutil.copy(sfnttool_jar, sfnttool_dest)
        else:
            log.log(log.ERROR, "no such file: %s" % sfnttool_jar)

    def finalize_options(self):
        pass


class CustomBuildCommand(build):
    """ Compile sfntly *.jar files before building the Python package.
    Skip build if all files defined in 'jar_files' variable already exists.
    """
    def run(self):
        dst_files = os.listdir(sfnttool_dest)
        if any([j for j in jar_files if j not in dst_files]):
            self.run_command("build_jar")
        build.run(self)


class CustomInstallCommand(install):
    """Run 'build' command before installing the Python package."""
    def run(self):
        self.run_command("build")
        install.run(self)


setup(name="sfntly",
      version="1.0",
      description="Python bindings for the sfntly library",
      author="Dalton Maag Ltd",
      author_email="it@daltonmaag.com",
      url="https://github.com/daltonmaag/sfntly-py",
      license="Private",
      package_dir={"": "Lib"},
      packages=['sfntly'],
      package_data={
              "sfntly": [
                      "sfntly-java-dist/sfnttool.jar",
                      "sfntly-java-dist/README.md"
                    ]
              },
      cmdclass={
            'clean': CleanJarCommand,
            'build_jar': BuildJarCommand,
            'build': CustomBuildCommand,
            'install': CustomInstallCommand
          }
      )
