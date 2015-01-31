#!/usr/bin/env bash

WORKER=$1
URL=$2


PROGRAM_ID=
INPUT_FILE=
OUTPUT_FILE=

if [ $# -ne 2 ];then
  echo "Usage: $0 worker_name url"
  exit 1
fi

#if [ -z "$TVENC_APIKEY" ];then
#  echo "Please set environment 'TVENC_APIKEY'" >&2
#  exit 1
#fi

get_new_program()
{
  json=`curl -F "worker=$WORKER" $URL/api/newjob/`
  if [ -z "$json" ];then
    return 1
  fi
  PROGRAM_ID=`echo "$json" | jq -r .id`
  INPUT_FILE=`echo "$json" | jq -r .input`
  OUTPUT_FILE=`echo "$json" | jq -r .output`
  echo $PROGRAM_ID
  echo $INPUT_FILE
  echo $OUTPUT_FILE
}



shutdown_handler()
{
  if [ -n "$PROGRAM_ID" ];then
    echo ""
  fi
  exit 100
}

trap shutdown_handler SIGINT

get_new_program

