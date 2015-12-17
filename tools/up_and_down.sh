#!/bin/bash

SOURCE='cache'

for (( i=5; i<=103; i++  )); do
  cat ${SOURCE} | grep "\-${i}\."  | head -1
  cat ${SOURCE} | grep "\-${i}\."  | tail -1
done
