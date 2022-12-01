# Asp Diagnose Tool

ASP model diagnose tool based on the theorem solver CLINGO 5.4.1. 

"diagnose" is an executable file which includes all necessary libraries as CLINGO 5.4.1. This file is only executable on MAC OS.
"diagnose_win.exe" is the executable file for windows systems including all libraries to run CLINGO 5.4.1.

To call and use the Python (python 3.6.15) scripts, a clingo (version 5.4.1) installation is necessary, which can be done by creating a Conda environment based on the predefined provided file in the environment direcotry:

```
cd environment
conda env create -f environment.yml 
conda activate diagnose 
```

If a python import of the tool is necessary, one can use the diagnose.py class to import into the related python script. The argument "settings" dictionalry for this class can be seen in main_diagnose.py (see optional arugments)

## Optional arguments:

| Argument | Argument | Description |
| ------ | ------ | ------ |
| --help | -h | show this help message and exit |
| --index | -i | index to identify actual call (E.g.: time, call counter, etc.) |
| --file | -f | load ASP model file |
| --path | -p | load ASP model directory path |
| --faultsize | -fault | size of faults to search |
| --hidediagoutput | -hidediag | hide diagnose output in terminal (no argument needed) |
| --output | -out | define output file name and path for CSV (overview result) and JSON (detailed results) / default path: actual directory and file name with date and time |
| --json | -j | JSON output file is written (no argument needed) |
| --csv | -c | CSV output file is written (no argument needed) |
| --answersets | -a | number of answer sets (0: all, 1: compute one answer set, 2: two answer sets, ... |
| --observation | -obs | add additional observation file to ground with ASP file (e.g.: example.pl) |
| --adapt | -adapt | adapt data (comment out all constraints ':- not no_ab(X)' |
| --strongfaults | -strongfaults | use argument to activate search for strong fault 'only' or 'without' constraints, if argument is not used strong faults constraints are not implemented. choices=["only", "without"] |

## Example using application diagnose in terminal (all dependencies inlcuded!):

application/diagnose --index "0" --path data/asp_test_data --faultsize 3 --answersets 0 --output filename --json --csv --hidediagoutput --strongfaults "only"

## Example usnig python code:

python model_diagnose.py --index "*" --path data/asp_test_data --faultsize 3 --answersets 0 --output filename --json --csv --strongfaults "without"
python model_diagnose.py --index "1" --file testfile.pl --faultsize 3 --answersets 0 --output filename --json --csv

## Output:

After the computation is finished, the data can be stored in a CSV (--csv) and JSON (--json) file based on the given output (--output) filename and path.
If the tool is called in a loop with the same output file name then it files got expanded with the new data. This is useful if for example the diagnose is performed on a time dependend system and for each timestep a diagnosis is executed. To track the call, use the index (--index) option. This allows for example to add the correlated timestep to identify the data. (e.g.: time: 0.01 -> index=0.01, time: 0.02 -> index=0.02, ...) 

### CSV
The header of the CSV data file:
"Index, Model,Time 0,Time 1,Time 2,Time 3,NoD 0,NoD 1,NoD 2,NoD 3,ASPDiagTime"

E.g.:
```
Index,Model,Time 0,Time 1,NoD 0,NoD 1,ASPDiagTime
0,test_heater_circuit.pl,0.007652997970581055,0.009721755981445312,0,1,0.017589092254638672
1,test_heater_circuit.pl,0.007380962371826172,0.010998964309692383,0,0,0.018507003784179688
2,test_heater_circuit.pl,0.007673025131225586,0.0077838897705078125,0,0,0.015599727630615234
```


### JSON
The JSON file is stored with file name and the related data with detailed diagnose results.

E.g.:
```
[
      {
            "0": {
                  "test_heater_circuit.pl": [
                        {
                              "diag time": 0.007652997970581055,
                              "fault size": 0,
                              "diag found": 0,
                              "diag": [],
                              "observation": [
                                    "val(int(tm),between(t_low, null),0)."
                              ]
                        },
                        {
                              "diag time": 0.009721755981445312,
                              "fault size": 1,
                              "diag found": 1,
                              "diag": [
                                    [
                                          "ab(sw)"
                                    ]
                              ],
                              "observation": [
                                    "val(int(tm),between(t_low, null),0)."
                              ]
                        }
                  ]
            }
      },
      {
            "1": {
                  "test_heater_circuit.pl": [
                        {
                              "diag time": 0.007380962371826172,
                              "fault size": 0,
                              "diag found": 0,
                              "diag": [],
                              "observation": [
                                    "val(int(tm),between(t_low, null),0).",
                                    "val(int(tm),between(t_low, null),1)."
                              ]
                        },
                        {
                              "diag time": 0.010998964309692383,
                              "fault size": 1,
                              "diag found": 0,
                              "diag": [],
                              "observation": [
                                    "val(int(tm),between(t_low, null),0).",
                                    "val(int(tm),between(t_low, null),1)."
                              ]
                        }
                  ]
            }
      },
      {
            "2": {
                  "test_heater_circuit.pl": [
                        {
                              "diag time": 0.007673025131225586,
                              "fault size": 0,
                              "diag found": 0,
                              "diag": [],
                              "observation": [
                                    "val(int(tm),between(t_low, null),0).",
                                    "val(int(tm),between(t_low, null),1).",
                                    "val(int(tm),between(t_low, null),2)."
                              ]
                        },
                        {
                              "diag time": 0.0077838897705078125,
                              "fault size": 1,
                              "diag found": 0,
                              "diag": [],
                              "observation": [
                                    "val(int(tm),between(t_low, null),0).",
                                    "val(int(tm),between(t_low, null),1).",
                                    "val(int(tm),between(t_low, null),2)."
                              ]
                        }
                  ]
            }
      }
]
```

## Generating executable file:
Use the conda environment to build the executable file for the related OS with the following command. 

```
cd app
pyinstaller --onefile main_diagnose.py --name diagnose
```
