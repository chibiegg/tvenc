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

set_program_status()
{
  status=$1
  curl -F "result=$status" $URL/api/update_status/$PROGRAM_ID/
  echo ""
}



shutdown_handler()
{
  if [ -n "$PROGRAM_ID" ];then
    set_program_status "cancel"
  fi
  exit 100
}

trap shutdown_handler SIGINT

while true
do
  PROGRAM_ID=
  INPUT_FILE=
  OUTPUT_FILE=
  get_new_program
  result=$?
  
  if [ $? -eq 0 ];then

    if [ -e "$INPUT_FILE" ]; then
      HandBrakeCLI -i "$INPUT_FILE" -o "$OUTPUT_FILE" -t 1 -c 1 -f mp4 --denoise="2:1.5:3:2.25" -w 1280 -l 720 \
                   --crop 0:0:0:0 --modulus 2 -e x264 -r 29.97 --detelecine -q 21 -a 1 -E faac -6 stereo -R Auto -B 128 -D 0 \
                   -x b-adapt=2:me=umh:merange=64:subq=10:trellis=2:ref=12:bframes=6:analyse=all:b-pyramid=strict:deblock=2,2 --verbose=1
      result=$?
    
      if [ $? -eq 0 ];then
        set_program_status "ok"
      else
        set_program_status "error"
      fi
    else
      set_program_status "cancel"
      echo "Input file '$INPUT_FILE' does not exists" >2&
      sleep 10
    fi
  fi
  
  sleep 5
  
done














