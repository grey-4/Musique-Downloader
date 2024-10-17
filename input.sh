#!/bin/bash
while getopts ":p:s:" opt; do
		case $opt in 
				s)
						input_s="$OPTARG"
                        python single.py -s "$input_s"
						;;
				p)
						input_p="$OPTARG"
						python dlr1.py -p "$input_p"
						;;
				\?)
						echo "Please provide an valid option: -$OPTARG" >&2
						exit 1
						;;
				:)
						echo "Option -$OPTARG requires an argument." >&2
						exit 1
						;;
		esac
done

