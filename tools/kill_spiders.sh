#!/bin/bash

#=================================================================
# Auther: Zacky
# Email:  zacky_su@zju.edu.cn
# Date: August 18th 2015
#
# Description: 'kill_spiders.sh' is used to kill specific spiders.
#
# Parameters:
#   ${1}: Log Name.
#
# Usage:
#   nohup ./kill_spiders.sh ${1} 2>&1 >> log/spiders_running.log &
#=================================================================

WORK_DIR_PREFIX='/home/zacky/Projects/Blotus/tasks/'  # NEED TO MODIFY HERE as /path/to/log/dir.
LOG_DIR=${WORK_DIR_PREFIX}'log/'
EXP_DIR=${WORK_DIR_PREFIX}'helpers/exporterHelper/'
TMP_CAE_FILE=${EXP_DIR}'cache'
PID_FILE=${LOG_DIR}${1}'.pid'
RET_FILE=${LOG_DIR}${1}'.ret'

if [[ $# -ne 1 ]]; then
  echo "ARGUMENTS ERROR."
  exit 1
fi

kill -9 `cat ${PID_FILE}`

echo "PID `cat ${PID_FILE}` PROCESS WAS KILLED SUCCESSFULLY."

if [ -f ${TMP_CAE_FILE} ]; then
  rm -f ${TMP_CAE_FILE}
fi

sleep 5

rm -rf ${PID_FILE} #${RET_FILE}
