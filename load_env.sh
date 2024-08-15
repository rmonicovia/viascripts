#!/usr/bin/bash

# TODO --export to prepend a "export " before every variable
# TODO Parameter to enclose values in "

help() {
  cat << EOF
$(basename $0): Load environment from a kubernets POD

Usage:
$(basename $0) <pod from "oc get pods"> <environment name>

Will return a error if environment already exists
EOF

  [ -n "$1" ] && exit $1
}

if [ "$1" == "-h" -o "$1" == "--help" ]; then
  help 0
fi

which oc &> /dev/null || {
  echo "FATAL: \"oc\" command MUST be present! quitting"
  exit 1
}

force=no
verbose=no

while (( $# )); do
  case "$1" in
    "--force" | "-f")
      force=yes
      shift 1
      ;;

    "--verbose" | "-v")
      verbose=yes
      shift 1
      ;;

    *)
      if [ -z "$pod" ]; then
        pod="$1"
      elif [ -z "$environment_name" ]; then
        environment_name="$1"
      else
        echo "Extra parameter: \"$1\", ignoring"
      fi

      shift 1
      ;;
  esac
done

environment_dir="${ENVIROMENT_DIR:-"$HOME/environments"}"
environment_file="$environment_dir/${environment_name}.env"

[ $verbose == yes ] && {
  echo "pod: $pod"
  echo "environment_dir: $environment_dir"
  echo "environment_name: $environment_name"
  echo "environment_file: $environment_file"
  echo "force: $force"
  echo "verbose: $verbose"
  echo
}


[ $force == no -a -e "$environment_file" ] && {
  echo "Error: environment file already exists, refusing to overwrite it"
  exit 1
}

cmd=(oc exec -t '"$pod"' -- /bin/sh -c env \| grep -Ev '$(cat "$environment_dir/system_variables.regex")' \| sort \> '"$environment_file"')

[ $verbose == yes ] && {
  echo "Running \"${cmd[@]}\""
}

eval "${cmd[@]}"

echo "Environment from pod \"$pod\" saved to \"$environment_file\""
