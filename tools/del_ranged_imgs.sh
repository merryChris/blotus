#!/bin/bash

folder='ttt/'

for (( i=${1}; i<=${2}; i++  )); do
  if [ -d "${folder}thread_${i}" ]; then
    rm -rf "${folder}thread_${i}"
    echo "Deleted Folder thread_${i}."
  fi
done
