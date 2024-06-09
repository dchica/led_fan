import numpy as np

#Allows script to run locally, adds entire directory to path
from pathlib import Path
import sys
root = Path(__file__).parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root.parent) not in sys.path:
    sys.path.append(str(root.parent))

#Load helper functions
from misc.load_misc import *

class Blade:
    '''
    Class to instantiate individual fan Blade

    Blade contains information on number of LEDs and positional data in 2D plane

    Has function to update current position based on delta time

    nleds: Number of LEDs to be used on blade

    ini_angle: Starting angle of blade when power is off

    justify: Determines whether to space out LEDs evenly along blade
    '''
    def __init__(self, nleds, ini_angle=0, justify=True):
        ##User Defined Params
        self.nleds = nleds
        self.ini_angle = ini_angle % 360 #degrees, starts on RHS like trig, default position when power off
        self.length = 20 #cm
        self.margin_center = 1 #cm
        self.margin_end = 3 #cm
        self.min_led_spacing = .5 #cm
        self.justify = justify #if True spreads leds evenly along blade, else from center out with min_led_spacing
        self.hz = 24 #rotations/sec
        
        ##Dependent Params
        self.cur_spacing = None #cm
        self.led_list = np.array([]) #[led1_pos, led2_pos, ...] #cm #ONLY RELATIVE TO BLADE - R in polar coordinates
        self.rot_time = None
        
        ##Position Data - Dependent
        self.cur_angle = self.ini_angle #degrees - Θ in polar coordinates
        self.cur_x = np.array([])  #[led1x_pos, led2x_pos, ...] #cm #ABSOLUTE POSITION - X in cartesian coordinates
        self.cur_y = np.array([])  #[led1y_pos, led2y_pos, ...] #cm #ABSOLUTE POSITION - Y in cartesian coordinates
        self.cur_vals = np.array([]) #[led1_val, led2_val, ...] #To be set externally by Fan class

        ##Autorun functions
        self.update_params(quiet=True)
        self.update_pos(delta_time=0)
        
    def update_params(self, quiet=False):
        '''
        Sets current spacing, led position list, and mean rotation time based on User Defined Params
        '''
        #spacing
        area = self.length - (self.margin_center + self.margin_end)
        if self.justify:
            self.cur_spacing = area / self.nleds
        else:
            self.cur_spacing = self.min_led_spacing
        
        #led_list
        self.led_list = np.arange(self.margin_center, self.margin_center+area, self.cur_spacing)
        
        if len(self.led_list) > self.nleds:
            self.led_list = self.led_list[:self.nleds]
        
        #rot_time
        self.rot_time = 1/self.hz

        #default LED vals
        self.reset_cur_vals()
        
        if not quiet:
            print('Blade Parameters Updated')

    def update_pos(self, delta_time, quiet=True):
        '''
        Uses delta time to update current angle and current x,y position of each LED in blade

        Dependent on current rot_time (and thus Hz value)

        quiet: Set to False if you want to print x,y positions (debug)
        '''
        #update angle
        delta_rot = delta_time/self.rot_time #sec*rot/sec = rots elapsed
        delta_angle = delta_rot * 360 % 360
        self.cur_angle += delta_angle

        #update pos
        self.cur_x = np.round(self.led_list * np.cos(rads(self.cur_angle)), 2) #.1mm precision
        self.cur_y = np.round(self.led_list * np.sin(rads(self.cur_angle)), 2) #.1mm precision
        
        if not quiet:
            print('Position Updated')
            print(f'x pos: {np.round(self.cur_x, 1)}')
            print(f'y pos: {np.round(self.cur_y, 1)}')

        return self.cur_x, self.cur_y
    
    def get_pos_angle(self, angle, quiet=False):
        '''
        Returns x,y position of each LED in blade at provided angle

        Does not update Blade data

        angle: Degrees

        quiet: Set to False if you want to print x,y positions (debug)
        '''
        #update pos
        cur_x = np.round(self.led_list * np.cos(rads(angle)), 2)
        cur_y = np.round(self.led_list * np.sin(rads(angle)), 2)
        
        if not quiet:
            print('Position Updated')
            print(f'x pos: {np.round(cur_x, 1)}')
            print(f'y pos: {np.round(cur_y, 1)}')

        return cur_x, cur_y

    def reset_cur_vals(self):
        '''
        Sets cur_vals array to all 0's
        '''
        self.cur_vals = np.zeros((self.nleds, 3), dtype=int) #Default RGB

##Debug
if __name__ == '__main__':
    B = Blade(nleds=10)
    print('Done')
        
        