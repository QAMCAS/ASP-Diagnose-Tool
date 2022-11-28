from math import ceil
import os

abs_path = "../data/"

class Diagnose:
    def __init__(self):
        self.val_obs_temp_init = "val(int(tm),"
        self.val_obs_temp = "val(int(tm),"
        self.val_obs_sw = "val(out(sw),"
        self.val_obs_sw_on_off = "off(sw"
        self.val_obs_heater = "val(out(h),"
        self.val_obs_battery = "val(out(bat),"
        
        self.obs_temp = [self.val_obs_temp_init + "null,0)."]
        self.obs_sw = [self.val_obs_sw + "null,0)."]
        self.obs_sw_type2 = [self.val_obs_sw_on_off + ",0)."]
        self.obs_heater = [self.val_obs_heater + "null,0)."]
        self.obs_battery = [self.val_obs_battery + "low,0)."]
        
        self.cnt_time = 0
        
    def temperature_logic(self, temperature):
        t_low = 10
        t_up = 20
        t_max = 22
        
        t = ceil(temperature)
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

    def switch_logic(self, switch):
        if switch == True:
            sw = "max"
        elif switch == False:
            sw = "null"
        else:
            sw = "null"
        return sw
    
    def switch_on_off_logic(self, switch):
        if switch == True:
            sw = "on(sw"
        elif switch == False:
            sw = "off(sw"
        else:
            sw = "off(sw"
        return sw

    def heater_logic(self, heater):
            
        if heater >= 80.0:
            h = "t_max"
        elif heater < 80.0 and heater > 0.0:
            h = "t_half"
        elif heater <= 0.0:
            h = "null"
        else:
            h = "null"
        
        return h

    def reset(self):
        self.obs_temp = [self.val_obs_temp_init + "null,0)."]
        self.obs_sw = [self.val_obs_sw + "null,0)."]
        self.obs_sw_on_off = [self.val_obs_sw_on_off + ",0)."]
        self.obs_heater = [self.val_obs_heater + "null,0)."]
        self.obs_battery = [self.val_obs_battery + "low,0)."]
        self.cnt_time = 0
        with open(abs_path + 'test_heater_obs.pl','w') as f:
            f.write("")
            f.close()
        with open('out.csv', 'w') as f:
            f.write("")
            f.close()
        with open('out.json', 'w') as f:
            f.write("")
            f.close()
 
    def observation_validator_all(self, logic, obs, obs_new):
        obs.insert(0, obs_new)
        if logic:
            if len(obs) > 2:
                obs.pop(-1)   
        else:
            if len(obs) > 1:
                obs.pop(-1)
        
        return obs
    
    def diagnose_all(self, time, temperature, switch, battery, heater):
    
        obs_temp_new = self.val_obs_temp + "{},{}).".format(self.temperature_logic(temperature), time-1)
        self.obs_temp = self.observation_validator_all(False, self.obs_temp, obs_temp_new)
        #self.obs_temp.append(obs_temp_new)
        
        obs_sw_new = self.val_obs_sw + "{},{}).".format(self.switch_logic(switch), time)
        self.obs_sw = self.observation_validator_all(True, self.obs_sw, obs_sw_new)
        #self.obs_sw.append(obs_sw_new)
        
        obs_sw_on_off_new = "{},{}).".format(self.switch_on_off_logic(switch), time)
        self.obs_sw_on_off = self.observation_validator_all(False, self.obs_sw_on_off, obs_sw_on_off_new)
        #self.obs_sw_on_off.append(obs_sw_on_off_new)
        
        obs_heater_new = self.val_obs_heater + "{},{}).".format(self.heater_logic(heater), time)
        self.obs_heater = self.observation_validator_all(True, self.obs_heater, obs_heater_new)
        #self.obs_heater.append(obs_heater_new)
        
        obs_battery_new = self.val_obs_battery + "{},{}).".format((battery), time)
        self.obs_battery = self.observation_validator_all(True, self.obs_battery, obs_battery_new)
        
        with open(abs_path + 'test_heater_obs.pl','w') as f:
            for obs in self.obs_temp:
                f.write(obs + '\n')
            #for obs in self.obs_sw:
            #    f.write(obs + '\n')
            for obs in self.obs_sw_on_off:
                f.write(obs + '\n')
            #for obs in self.obs_heater:
            #    f.write(obs + '\n')
            #for obs in self.obs_battery:
            #    f.write(obs + '\n')
            
            #if time > 1:
                #f.write("time({}).".format(time) + '\n')
                #f.write("time({}).".format(time-1) + '\n')
            #else:
                #f.write("time(0)." + '\n')
            
            f.close()
            self.cnt_time +=1
            
        config= "--index {} -f ../data/test_heater_simple.pl -a 5  --faultsize 1 --observation ../data/test_heater_obs.pl --output out --csv --json".format(time)
        os.system("python ../app/main_diagnose.py " + config)