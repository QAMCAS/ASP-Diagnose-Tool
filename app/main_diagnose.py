import os
import fnmatch
from datetime import datetime
import sys
import argparse

import adapt_data
from diagnose import Diagnose


def main(settings):
    
    # settings{
    # 'files': ['data/asp_test_data/c432_tc_1_1 2.pl'], 
    # 'index':  '*'
    # 'answers': '0',
    # 'faultSize': '0',
    # 'showDiagInTerminal': True, 
    # 'outputFile': './diagnose_data_15-03-2022_14:17:55', 
    # 'isWrite2Csv': False, 
    # 'isWrite2Json': False, 
    # 'strong_fault_only': False, 
    # 'strong_fault_without': False, 
    # 'strong_faults': False
    # 'observation': "path to file"'
    # }
    diag = Diagnose(settings)
    diag.compute(index=settings["index"])
             
if __name__ == "__main__":

    file = ""
    size = 0
    files = []
    path = ""
    adapt = False
    settings = dict()

    # Initiate the parser
    parser = argparse.ArgumentParser()

    # Add long and short argument
    parser.add_argument("--file", "-f", type=str, help="load ASP file")
    parser.add_argument("--index", "-i", help="data index for different calls")
    parser.add_argument("--output", "-out", type=str, help="define output file path for CSV (overview result) and JSON (detailed results) / default path: actual directory")
    parser.add_argument("--csv", "-c", action="store_true", help="CSV output file is written (no argument needed)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output file is written (no argument needed)")
    parser.add_argument("--path", "-lp", type=str, help="load ASP directory path")
    parser.add_argument("--faultsize", "-fault", type=int, help="size of faults to search")
    parser.add_argument("--hidediagoutput", "-hidediag", action="store_true", help="hide diagnose output in terminal (no argument needed)")
    parser.add_argument("--answersets", "-a", type=int, help="number of answer sets \
        (0: all, 1: compute one answer set, 2: two answer sets, ...")
    parser.add_argument("--observation", "-obs", type=str, help="add additional observation file to ground with ASP file")
    parser.add_argument("--adapt", "-adapt", action="store_true", help="adapt data (no argument needed) - comment out all constraints ':- not no_ab(X)' \
        This option is only available when a path to the files is given, not for a single file. ")
    parser.add_argument("--strongfaults", "-strongfaults", type=str, choices=["only", "without"], help="use argument to activate search for strong fault 'only' or 'without' constraints, if argument is not used strong faults constraints are not implemented.")

    # Read arguments from the command line
    args = parser.parse_args()

    if args.index:
        settings.update({"index":args.index})
    else:
        settings.update({"index":"*"})
        
    if args.file:
        file = args.file
        settings.update({"files":[file]})
        
    elif args.path:
        path = args.path
        if(path[-1] != '/'):
                path += '/'
        listOfFiles = os.listdir(path)
        pattern = "*.pl"
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern):
                files.append(path+entry)
                
        settings.update({"files":files})
    else:
        print("(!) no file(s) selected")
        sys.exit(1)
        
    if args.faultsize:
        size = int(args.faultsize)+1
    else:
        size = 0
    
    settings.update({"faultSize":size})
        
    if args.answersets:
        answers = str(args.answersets)
    else:
        answers = "0"
    
    settings.update({"answers":answers})
    
    if args.adapt and args.path:
        adapt = bool(args.adapt)

    if adapt:
        adapt_data.startAdaption(path)

    if args.hidediagoutput:
        showDiagInTerminal = False
    else: 
        showDiagInTerminal = True
    
    settings.update({"showDiagInTerminal":showDiagInTerminal})
    
    if args.output:
        outputFile = str(args.output)
    else:
        isWrite2Csv = False
        isWrite2Json = False
        now = datetime.now()
        outputFile = "." + '/diagnose_data_' + now.strftime("%d-%m-%Y_%H:%M:%S")
    
    settings.update({"outputFile":outputFile})
    
    if args.csv:
        isWrite2Csv = bool(args.csv)
    else: 
        isWrite2Csv = False
        
    settings.update({"isWrite2Csv":isWrite2Csv})
    
    if args.json:
        isWrite2Json = bool(args.json)
    else: 
        isWrite2Json = False
    
    settings.update({"isWrite2Json":isWrite2Json})
    
    if args.strongfaults:
        strong_faults = True
        if str(args.strongfaults) == "only":
            strong_fault_only = True
            strong_fault_without = False
        elif str(args.strongfaults) == "without":
            strong_fault_without = True
            strong_fault_only = False
        else:
            strong_faults = False
            strong_fault_without = False
            strong_fault_only = False
    else:
        strong_faults = False
        strong_fault_without = False
        strong_fault_only = False
        
    settings.update({"strong_fault_only":strong_fault_only})
    settings.update({"strong_fault_without":strong_fault_without})
    settings.update({"strong_faults":strong_faults})
    
    obsfile = ""
    if args.observation:
        obsfile = args.observation
    else:
        obsfile=""
    settings.update({"observation":obsfile})
    
    main(settings)
