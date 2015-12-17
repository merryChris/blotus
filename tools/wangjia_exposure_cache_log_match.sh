#!/bin/bash

SOURCE='cache'
TARGET='log'

while read LINE; do
  RES=`cat ${TARGET} | grep ${LINE}`
  if [ $? -ne 0 ]; then
    echo ${LINE}
  fi
done < ${SOURCE}
