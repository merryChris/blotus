#!/bin/bash

#=================================================================================
# Auther: Zacky
# Email:  zacky_su@zju.edu.cn
# Date: August 14th 2015
#
# Description: 'start_spiders.sh' is used to start spiders in DIFFERENT project.
#
# Parameters:
#   ${1}: Project Namespace Spiders Belongs to.
#   ${2}: Spider Name.
#   ${3}: Log Name.
#   ${4}-: Arguments.
#
# Usage:
#   nohup ./start_spiders.sh ${1} ${2} ${3} {4}- 2>&1 >> log/spiders_running.log &
#=================================================================================

WORK_DIR_PREFIX='/home/zacky/Projects/Blotus/tasks/'  # NEED TO MODIFY HERE as /path/to/log/dir.
LOG_DIR=${WORK_DIR_PREFIX}'log/'
EXP_DIR=${WORK_DIR_PREFIX}'helpers/exporterHelper/'
PROJECT_NAME=${1}
SPIDER_NAME=${2}
SELECT_COUNT_FILE=${WORK_DIR_PREFIX}'tools/select_count.py'
URL_SPIDER_MAPPING_FILE=${WORK_DIR_PREFIX}'tools/url_spider_mapping.py'
TMP_CAE_FILE=${EXP_DIR}'cache'
PID_FILE=${LOG_DIR}${3}'.pid'
CAE_FILE=${LOG_DIR}${3}'.cae'
LOG_FILE=${LOG_DIR}${3}'.log'
RET_FILE=${LOG_DIR}${3}'.ret'

ARGS_NUM=`expr ${#} - 3`

#echo $$ > ${PID_FILE}
function write_log() {
  local log_txt=${1}
  echo "`date "+%Y-%m-%d %H:%M:%S"` ${log_txt}"
}

function check_args_number() {
  if [[ ${1} -ne ${ARGS_NUM} ]]; then
    write_log "ARGUMENTS ERROR."
    exit 1
  fi
}

function select_count() {
  echo `python ${SELECT_COUNT_FILE} ${PROJECT_NAME} ${SPIDER_NAME}`
  wait
}

function url_spider_mapping(){
  echo `python ${URL_SPIDER_MAPPING_FILE} ${PROJECT_NAME} ${SPIDER_NAME}`
  wait
}

function gen_cache() {
  write_log "ACCESSING TO EXPORTER HELPER DIRECTORY '${EXP_DIR}'."
  cd "${EXP_DIR}"

  write_log "COMMAND '${GEN_CACHE_CMD}' IS RUNNING."
  eval $GEN_CACHE_CMD
  echo $! > ${PID_FILE}
  wait $!
  sleep 5
  if [ -f ${TMP_CAE_FILE} ]; then
    mv ${TMP_CAE_FILE} ${CAE_FILE}
  fi
  write_log "COMMAND '${GEN_CACHE_CMD}' ENDED."
}

function run_spider() {
  if [ ! -z "${GEN_CACHE_CMD}" -a ! -f ${CAE_FILE} ]; then
    write_log "CACHE FILE DOESN'T EXIST."
    return 1
  fi

  write_log "ACCESSING TO WORKING DIRECTORY '${WORK_DIR_PREFIX}${PROJECT_NAME}'."
  cd "${WORK_DIR_PREFIX}${PROJECT_NAME}"

  ORI_CNT=`select_count`
  write_log "COMMAND '${SPIDER_CMD}' IS RUNNING."
  eval $SPIDER_CMD
  echo $! > ${PID_FILE}
  wait $!
  write_log "COMMAND '${SPIDER_CMD}' ENDED."
  NEW_CNT=`select_count`
}

function output_stats() {
  if [ ! -f ${LOG_FILE} ]; then
    write_log "NO RESULT FILE YET."
    return 1
  fi

  SUCCESS=`expr ${NEW_CNT} - ${ORI_CNT}`
  ERROR=`cat ${LOG_FILE} | grep 'ERROR\|WARNING' | wc -l`
  echo "{\"SUCCESS\": ${SUCCESS}, \"ERROR\": ${ERROR}, \"ORI_CNT\": ${ORI_CNT}, \"NEW_CNT\": ${NEW_CNT}}" > ${RET_FILE}
}

ORI_CNT=-1
NEW_CNT=-1
GEN_CACHE_CMD=
SPIDER_CMD=
URL_SPIDER=

#wangjia/wangjia/spiders/daohang.py
if [ "${SPIDER_NAME}"x = "daohang"x ]; then
  check_args_number 0
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  run_spider
  output_stats
fi

#wangjia/wangjia/spiders/dangan.py
if [ "${SPIDER_NAME}"x = "dangan"x ]; then
  check_args_number 2
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} -a from_id=${4} -a to_id=${5} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  run_spider
  output_stats
fi

#wangjia/wangjia/spiders/wenti.py
if [ "${SPIDER_NAME}"x = "wenti"x ]; then
  check_args_number 0
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  run_spider
  output_stats
fi

#wangjia/wangjia/spiders/wenti2.py
if [ "${SPIDER_NAME}"x = "wenti2"x ]; then
  check_args_number 0
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  run_spider
  output_stats
fi

#wangjia/wangjia/spiders/pingji.py
if [ "${SPIDER_NAME}"x = "pingji"x ]; then
  check_args_number 3
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} -a from_id=${4} -a to_id=${5} -a end_time=${6} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  run_spider
  output_stats
fi

#wangjia/wangjia/spiders/pingji2.py
if [ "${SPIDER_NAME}"x = "pingji2"x ]; then
  check_args_number 1
  URL_SPIDER=`url_spider_mapping`
  GEN_CACHE_CMD="nohup scrapy crawl ${URL_SPIDER} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} -a timestamp=${4} -a cache=${CAE_FILE} --loglevel=INFO >>${LOG_FILE} 2>&1 &"
  gen_cache
  run_spider
  output_stats
fi

#wangjia/wangjia/spiders/shuju.py
if [ "${SPIDER_NAME}"x = "shuju"x ]; then
  check_args_number 2
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} -a from_date=${4} -a to_date=${5} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  run_spider
  output_stats
fi

#wangjia/wangjia/spiders/xinwen.py
if [ "${SPIDER_NAME}"x = "xinwen"x ]; then
  check_args_number 3
  URL_SPIDER=`url_spider_mapping`
  GEN_CACHE_CMD="nohup scrapy crawl ${URL_SPIDER} -a from_id=${4} -a to_id=${5} -a category=${6} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} -a category=${6} -a cache=${CAE_FILE} --loglevel=INFO >>${LOG_FILE} 2>&1 &"
  gen_cache
  run_spider
  output_stats
fi

#wangjia/wangjia/spiders/baoguang.py
if [ "${SPIDER_NAME}"x = "baoguang"x ]; then
  check_args_number 2
  URL_SPIDER=`url_spider_mapping`
  GEN_CACHE_CMD="nohup scrapy crawl ${URL_SPIDER} -a from_id=${4} -a to_id=${5} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} -a cache=${CAE_FILE} --loglevel=INFO >>${LOG_FILE} 2>&1 &"
  gen_cache
  run_spider
  output_stats
fi

#helpers/imageHelper/imageHelper/spiders/grabber.py
if [ "${SPIDER_NAME}"x = "grabber"x ]; then
  check_args_number 5
  SPIDER_CMD="nohup scrapy crawl ${SPIDER_NAME} -a from_id=${4} -a to_id=${5} -a category=${6} -a model=${7} -a field=${8} --loglevel=INFO >${LOG_FILE} 2>&1 &"
  run_spider
  output_stats
fi

if [ -f "${PID_FILE}" ]; then
  rm -f ${PID_FILE}
fi

if [ -f "${CAE_FILE}" ]; then
  rm -f ${CAE_FILE}
fi

exit 0
