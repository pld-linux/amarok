#!/bin/sh
set -x
pkg=amarok
branch=1.4
tag=fdfafa156c9cda88ed3c045445548e4ca2b129bd
#tag=8cdcf9d8b634763b515c419805e98e9aa9107224
#tag=be0564032fc09a9ad6e5e3f22447e3582473904d
url=git://gitorious.org/amarok/history.git

if [ ! -d git ]; then
	git clone $url git
	cd $pkg
		git checkout -b $branch origin/$branch
	cd ..
fi

cd git
	git pull
	git diff $tag > ../$pkg-branch.diff
cd ..
