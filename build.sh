#!/bin/sh

# get absolute path to current script
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd )"

# path to compiled sfnttool.jar
sfnttool_jar="$SCRIPTPATH/vendor/sfntly/java/dist/tools/sfnttool/sfnttool.jar"

# go to java source folder and re-compile sfntly
cd "$SCRIPTPATH/vendor/sfntly/java"
ant clean dist

if [ -e "$sfnttool_jar" ]
then
	# move compiled jar inside python package
	cp "$sfnttool_jar" "$SCRIPTPATH/Lib/sfntly/sfntly-java-dist/"
else
	echo "ERROR: $sfnttool_jar not found!"
fi
