#!/bin/sh
PRJ=project$1
git checkout -b $PRJ
mkdir $PRJ
cd $PRJ
cp "$2" $PRJ.sql
git add $PRJ.sql
git commit 
git push origin $PRJ
