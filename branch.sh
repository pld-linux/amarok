#!/bin/sh
# http://gitorious.org/amarok/history/commits/1.4
set -x
pkg=amarok
branch=1.4
tag=fdfafa156c9cda88ed3c045445548e4ca2b129bd
url=git://gitorious.org/amarok/history.git

filter() {
	set -x
	# - was not present in tarball
	# see release_scripts/RELEASE_HOWTO for more exceptions
	filterdiff -x "a/src/engine/gst10/*" | \
	cat
}


if [ ! -d git ]; then
	git clone $url git
	cd $pkg
		git checkout -b $branch origin/$branch
	cd ..
fi

cd git
	git pull
	git diff $tag | filter > ../$pkg-branch.diff
cd ..
