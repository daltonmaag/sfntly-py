#!/usr/bin/env python

from setuptools import setup, Command
from setuptools.command.install import install
from distutils import log
import subprocess
import os
import shutil


__dirname__ = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


class CustomInstallCommand(install):
    """ Customized install command that builds "sfnttool.jar" from source
    before installing the python package.
    """
    def run(self):
        self.run_command("build_jar")
        install.run(self)


class BuildJarCommand(Command):

    description = "Build sfntly Java sources"

    user_options = []

    def initialize_options(self):
        pass

    def run(self):
        log.log(log.INFO, "Running `ant clean dist` to compile sfntly...")
        java_src_dir = os.path.join(
            __dirname__, "vendor", "sfntly", "java")
        sfnttool_jar = os.path.join(
            java_src_dir, "dist", "tools", "sfnttool", "sfnttool.jar")
        sfnttool_dest = os.path.join(
            __dirname__, "Lib", "sfntly", "sfntly-java-dist")
        os.chdir(java_src_dir)
        os.system('ant clean dist')
        os.chdir(__dirname__)
        if os.path.exists(sfnttool_jar):
            shutil.copy(sfnttool_jar, sfnttool_dest)
        else:
            log.log(log.ERROR, "No such file: %s" % sfnttool_jar)

    def finalize_options(self):
        pass


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
            'build_jar': BuildJarCommand,
            'install': CustomInstallCommand
          }
      )
