#!/bin/bash

function usage {
    echo "Usage: bash run_analysis.sh [-t <Topic>] [-n <Question Number>]"
    echo "  Topic: Choose topic between 1 (Metadata), 2 (MIC). Default set to 1"
    echo "  Number: Choose question number between 1 - 5. Default set to 1"
    exit 1
}


if [ "$*" == "" ]; then
    echo "No argument provided"
    usage
fi

while getopts ":t:n:" opt; do
    case "${opt}" in 
        t)
            TOPIC=${OPTARG}
            ;;
        n)
            NUMBER=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done

python3 main.py -t ${TOPIC} -n ${NUMBER}
