#!/bin/bash
ruby -rubygems $1

grep -ho "@speaker_id=\"[A-Z][0-9]*\"" outputfile.log > speaker.log
grep -ho "\"[A-Z][0-9]*\"" speaker.log > filtered.log

grep -ho "@duration=[0-9]*\.[0-9]*" outputfile.log > duration.log 
grep -ho "[0-9]*\.[0-9]*" duration.log >> filtered.log

grep -ho "@start=[0-9]*\.[0-9]*" outputfile.log > start.log
grep -ho "[0-9]*\.[0-9]*" start.log>> filtered.log

rm speaker.log duration.log start.log outputfile.log




