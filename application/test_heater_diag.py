import os

# INPUT SIGNAL
#signal = [0,0,5,6,7,9,10,11,12,16,18,19,20,21,20,19,18,17,12,10,9,10,12]
signal = [0,0,5,6,7,9,10,11,9,8,8,8,8,8,8,8,8,8,8,8]
#signal =    [[0,0,16,18,19,20,21,20,19,18],\
#            [0,0,16,18,19,20,21,20,19,18,19,20,21,20],\
#            [0,0,16,18,18,18,18,18,18,18,18,18]]

# Transform temperature into logic sentence
def signal_logic(temperature):
    t_low = 10
    t_up = 20
    t_max = 20.5

    print("temp:", temperature)
    t = temperature
    value = "null"

    if t == 0:
        value = "null"
    elif t > 0 and t < t_low:
        value = "between(t_low, null)"
    elif t == t_low:
        value = "t_low"
    elif t > t_low and t < t_up:
        value = "between(t_up, t_low)"
    elif t == t_up:
        value = "t_up"
    elif t > t_up and t < t_max:
        value = "between(t_max, t_up)"
    elif t >= t_max:
        value = "t_max"

    return value

def reset():
    with open('../data/test_heater_obs.pl','w') as f:
        f.write("")
        f.close()
    with open('out.csv', 'w') as f:
        f.write("")
        f.close()
    with open('out.json', 'w') as f:
        f.write("")
        f.close()

def observation_limiter(obs, obs_new):
    obs.insert(0, obs_new)
    if len(obs) > 2:
            obs.pop(-1)       
    return obs
      
def diagnose(time, signal):
    global observation
              
    obs_new = "val(int(tm),{},{}).".format(signal_logic(signal), time)
    observation = observation_limiter(observation, obs_new)

    with open('../data/test_heater_obs.pl','w') as f: 
        for obs in observation:
            f.write(obs + '\n')
        f.close()
        
    config= "--index {} -f ../data/test_heater_circuit.pl -a 1  --faultsize 3 --observation ../data/test_heater_obs.pl --output out --csv --json".format(time)
    
    # use diagnose with python scripts
    os.system("python ../app/main_diagnose.py " + config)
    
    # using the executable on MAC or Lin
    #os.system("./diagnose " + config)
    
    #using the executable on Win 
    #os.system("diagnose_win.exe " + config)

time = 0
reset()
observation = []

for sig in signal:
    diagnose(time, sig)
    time += 1
