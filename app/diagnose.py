import clingo
import csv
import time
import os
import additional_rules
import json

class Diagnose:
    def __init__(self, settings):
        self.settings = settings
        self.constraintList = []
        self.atomList = []
        self.diagnoseList = []
        self.diagRun = 0
        self.isModelSatisfied = False
        self.diagDict = []
        self.analysisData = []
        
        if self.settings["isWrite2Csv"]:
            file = open(self.settings["outputFile"] + '.csv', 'a+')
            file.close()
            
            if os.stat(self.settings["outputFile"] + '.csv').st_size == 0:
                header = ['Index', 'Model']
                for r in range(self.settings["faultSize"]):
                    header.append('Time {}'.format(r))
                for r in range(self.settings["faultSize"]):
                    header.append('NoD {}'.format(r))
                header.append('ASPDiagTime')
            
                with open(self.settings["outputFile"] + '.csv', "a") as output:
                    writer = csv.writer(output)
                    writer.writerow(header)
                    output.close()
        
        if self.settings["isWrite2Json"]:
            file = open(self.settings["outputFile"] + '.json', 'a+')
            file.close()
            
            if os.stat(self.settings["outputFile"] + '.json').st_size == 0:
                with open(self.settings["outputFile"] + '.json', 'a') as output:
                    output.write("")
                    output.close()
                
    # the function compute includes all loops and functions calls 
    def compute(self, index="*"):
        fileNumber = 0
        diagnoseDict = {index:dict()}
        analysisData = []
        observation_list = list()

        for file in self.settings["files"]:
            fileNumber += 1
            self.diagRun = 0
            self.diagnoseList = []
            startTime = time.time()
            diagnoseTime = []
            diagnoseNumber = []
            self.constraintList = []
            print("\n>>>")
            print("(*)", fileNumber, "/", len(self.settings["files"]), "->", file)
            self.isModelSatisfied = False
            diagnoseDict[index].update({file:[]})

            for i in range(self.settings["faultSize"]):
                observation_list = []
                self.diagRun = i
                startTimeFaults = time.time()
                ctl = clingo.Control([self.settings["answers"]])
                ctl.load(file)
                
                # add additional observations from file
                if self.settings["observation"] != "":
                    if os.stat(self.settings["observation"]).st_size > 0:
                        with open(self.settings["observation"]) as f:
                            obs_lines = f.readlines()
                            for obs_line in obs_lines:
                                ctl.add("base", [], obs_line.strip())
                                observation_list.append(obs_line.strip())

                cnt = 0
                for cList in self.constraintList:
                    cnt += len(cList)
                    for c in cList:
                        ctl.add("base", [], c)

                faultSizeConstraint = str(":- not no_ab({}).").format(i)
                ctl.add("base", [], faultSizeConstraint)

                if self.settings["strong_faults"]:
                    if self.settings["strong_fault_only"]:
                        add_rule = additional_rules.solutions_strong_fault()
                    elif self.settings["strong_fault_without"]:
                        add_rule = additional_rules.solutions_without_strong_fault()
                    ctl.add("base", [], add_rule)
            
                ctl.ground([("base", [])])
                ctl.solve(on_model=self.__on_model, on_finish=self.__on_finish)
            
                del ctl
                
                diagnoseTime.append(time.time() - startTimeFaults)
                diagnoseNumber.append(len(self.diagnoseList[self.diagRun]))
                
                if self.is_satisfied:
                             
                    if self.is_satisfied:
                        satisfied = "model satisfied"
                    else:
                        satisfied = "model unsatisfied"  
                    
                    diagnoseDict[index][file].append({ 
                                                "model status": satisfied,
                                                "diag time": diagnoseTime[self.diagRun],
                                                "fault size": self.diagRun, 
                                                "diag found": len(self.diagnoseList[self.diagRun]), 
                                                "diag": self.diagnoseList[self.diagRun],
                                                "observation": observation_list})

                # check if model is in health state then stop
                if self.diagRun == 0 and self.is_satisfied:
                    break

            self.computationTime = time.time() - startTime

            analysisData.append(self.__collectData(index, file, diagnoseTime, diagnoseNumber, self.computationTime))
            
        if self.settings["isWrite2Csv"]:
            self.__writeData2Csv(self.settings["outputFile"], analysisData)
        if self.settings["isWrite2Json"]:
            self.__writeData2Json(self.settings["outputFile"], diagnoseDict)
        if self.settings["showDiagInTerminal"]:
            self.__print_to_terminal(diagnoseDict)

    # handle clingo solve answer sets
    def __on_model(self, m):
        atoms = []
        for atom in m.symbols(atoms=True):
            if "ab" == str(atom)[0:2]:
                atoms.append(str(atom))
        self.atomList.append(atoms)

    def __buildConstraint(self):
        constraints = []
        constraint = ""
        for atom in self.atomList:
            constraint = ":- "
            for num in range(self.diagRun):
                constraint += str("{}, ").format(atom[num])
            constraint = constraint[:-2] + "." 
            constraints.append(constraint)
            constraint = ""

        if len(constraints) > 0:
            self.constraintList.append(constraints)

    def __on_finish(self, m):
        self.is_satisfied = False
        #for diagAtom in atomList:
            #print("   diagnose [", diagRun, "]:", diagAtom)

        self.__buildConstraint()
        self.diagnoseList.append(self.atomList)
        self.atomList = []
        
        if str(m) == "SAT":
            self.is_satisfied = True
        elif str(m) != "SAT":
            self.is_satisfied = False

    def __collectData(self, index, file, diagnoseTime, diagnoseNumber, totalTime):
        tmp = []
        tmp.append(index)
        tmp.append(file)
        for t in diagnoseTime:
            tmp.append(t)
        for n in diagnoseNumber:
            tmp.append(n)
        tmp.append(totalTime)

        return tmp

    def __writeData2Csv(self, outFile, analysisData):

        self.analysisData.append(analysisData)
        with open(outFile+ '.csv', "a") as output:
            writer = csv.writer(output)
            for data in self.analysisData:
                writer.writerows(data)
            output.close()

    def __writeData2Json(self, outFile, diagDict):   
        #self.diagDict.append(diagDict)
        diagDict = diagDict
        d = []
        if os.stat(outFile + '.json').st_size == 0:
            with open(outFile + '.json') as f:
                d.append(diagDict)
                f.close()
        else:
            with open(outFile + '.json') as f:
                d = json.load(f)
                d.append(diagDict)
                f.close()

        with open(outFile + '.json', 'w') as output:
            output.write(json.dumps(d, indent = 6))
            output.close()
    
    def __print_to_terminal(self, information):
        for seq, diagnose in information.items():
            print("============================")
            print("Sequence:", seq)
            for key, value in diagnose.items():
                #print("Model file:", key)
                print("============================")
                for val in value:
                    print("Fault size:", val["fault size"])
                    print("Model Status:", val["model status"])
                    print("Observation:")
                    print("----------------------------")
                    print('\n'.join(['%i:\t%s' % (n+1, val["observation"][n]) for n in range(len(val["observation"]))]))
                    print("----------------------------")
                    print("Diag found:", val["diag found"])
                    print("Diagnose:")
                    print("----------------------------")
                    print('\n'.join(['%i:\t%s' % (n+1, val["diag"][n]) for n in range(len(val["diag"]))]))
                    print("----------------------------")
                    print("Diag time:", "{:f}".format(val["diag time"]), "sec")
            print("----------------------------")
            print("(!) Total time: ", "{:f}".format(self.computationTime), "sec")
            print("(!) Finished with diagnose of all files ...")