#!/bin/bash

VERBOSE=0

# 
# arg parsing
# from https://medium.com/@Drew_Stokes/bash-argument-parsing-54f3b81a6a8f
#
PARAMS=""
while (( "$#" )); do
  case "$1" in
    -v|--verbose)
      VERBOSE=1
      shift 1
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done
# set positional arguments in their proper place
eval set -- "$PARAMS"

if [ $VERBOSE -eq 1 ]
then
	VERBOSE_FLAG="-v"
else
	VERBOSE_FLAG=""
fi

# args: module_dir
function doctest_module () {
	python3 -m doctest $1 $VERBOSE_FLAG
}

#
# start testing
#
doctest_module splendor/core.py 
doctest_module splendor/game.py 
doctest_module splendor/player.py 

