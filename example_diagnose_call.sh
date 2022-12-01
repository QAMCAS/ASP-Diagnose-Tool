#!/bin/bash

./app/dist/diagnose --index 0 -f data/asp_test_data/c499_tc_2_16.pl -a 0 --faultsize 3 --output testout --json --csv
./app/dist/diagnose --index 1 -f data/asp_test_data/c499_tc_2_16.pl -a 0 --faultsize 3 --output testout --json --csv
./app/dist/diagnose --index 2 -f data/asp_test_data/c499_tc_2_16.pl -a 0 --faultsize 3 --output testout --json --csv
./app/dist/diagnose --index 3 -f data/asp_test_data/c499_tc_2_16.pl -a 0 --faultsize 3 --output testout --json --csv
./app/dist/diagnose --index 4 -f data/asp_test_data/c499_tc_2_16.pl -a 0 --faultsize 3 --output testout --json --csv