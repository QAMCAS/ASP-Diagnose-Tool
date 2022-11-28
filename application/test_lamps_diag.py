import os

import heater_diagnose as diag

abs_path = "../data/"

# Simulation
lamp1 =   [0,1,0,1,1,1,0]
lamp2 =   [0,1,1,0,1,1,0]
switch =  [0,1,1,1,0,1,1]
battery = [1,1,1,1,1,0,1]
    
# Signal Logic
def lamp_logic(lamp):
    if lamp:
        return "on"
    else:
        return "off"

def switch_logic(sw):
    if sw:
        return "on(s)."
    else:
        return "off(s)."
    
# Output file reset
def reset():
    with open(abs_path + 'test_lamps_obs.pl','w') as f:
        f.write("")
        f.close()
    with open('out.csv', 'w') as f:
        f.write("")
        f.close()
    with open('out.json', 'w') as f:
        f.write("")
        f.close()

def write_observations(observations):  
    with open(abs_path + 'test_lamps_obs.pl','w') as f:
        for obs in observations:
            f.write(obs+ '\n')
    f.close()
         
def main():
    
    for i in range(len(switch)):
        obs_lamp_1 = "val(light({}),{}).".format("l1",lamp_logic(lamp1[i]))
        obs_lamp_2 = "val(light({}),{}).".format("l2",lamp_logic(lamp2[i]))
        obs_sw = switch_logic(switch[i])
        write_observations([obs_lamp_1, obs_lamp_2, obs_sw])
        
        config= "--index {} -f ../data/two_lamps_example_orig.pl -a 5 --faultsize 3 --observation ../data/test_lamps_obs.pl --output out --csv --json".format(i)
        os.system("python ../app/main_diagnose.py " + config)

if __name__ == '__main__':
    reset()
    main()
