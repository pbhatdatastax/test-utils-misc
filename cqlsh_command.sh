#!/bin/bash
set -euo pipefail


echoerr() { echo "$@" 1>&2; }
badopt() { echoerr "$@"; help='true'; }
opt() { if [[ -z ${2-} ]]; then badopt "$1 flag must be followed by an argument"; fi; export $1="$2"; }
required_args() { for arg in $@; do if [[ -z "${!arg-}" ]]; then badopt "$arg is a required argument"; fi; done; }

while [[ $# -gt 0 ]]; do
  arg="$1"
  case $arg in
    -c|--cluster) shift; opt cluster "$1"; shift;;	    
    -t|--token)       shift; opt token "$1"; shift;;
    -b|--bundle)   shift; opt bundle "$1"; shift;;
    -h|--help)                 opt help true; shift;;
    *) cluster_id=$arg; shift;;
  esac
done

if [[ -z ${help-} ]]; then
  required_args cluster token bundle
fi

if [[ -n ${help-} ]]; then
  echoerr "Usage: $0"
  echoerr "    -c, --cluster       <cluster>     AstraCS UUID for DB"
  echoerr "    -t, --token       <token>     AstraCS token for DB"
  echoerr "    -b, --bundle   <bundle>    secure connect bundle to read from"
  echoerr "    -h, --help"
  exit 1
fi

if  [ ! -f $bundle ]; then
 curl -SL --header 'Accept: application/json' --header "Authorization: Bearer $token" -X POST  "https://api.astra.datastax.com/v2/databases/$cluster/secureBundleURL" -s|jq '.downloadURL'|xargs curl -o $bundle
 service datadog-agent restart
fi

out=$(/opt/datadog-agent/cqlsh-astra/bin/cqlsh -p $token -u token -b $bundle -e "select release_version from system.local" 2> /dev/null || true)
out=$(echo $out|/bin/awk '{print $3}'|cut -d "." -f1)
#echo $avail
re='^[0-9]+$'
#echo $out
out=`echo -n $out`
if [[ $out =~ $re ]] ; then
	echo -n $out
else
	echo -n 0
fi

