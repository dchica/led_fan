from pathlib import Path
import sys
root = Path(__file__).parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root.parent) not in sys.path:
    sys.path.append(str(root.parent))

import numpy as np
import cv2 as cv
from matplotlib.axes import Axes
import matplotlib.pyplot as plt

import time

from misc.load_misc import *
from classes.blade import Blade
from classes.imager import Imager

class Fan:
    def __init__(self, nleds, nblades, freq, img_path='', mode='inscribe'):
        ##User Defined Params
        self.nleds = nleds
        self.nblades = nblades
        self.freq = freq
        self.mode = mode
        self.img_path = img_path

        ##Dependent Params
        self.img = np.array([[]])
        self.blade_list: list[Blade] = []
        self.imager: Imager = None

        ##Autorun Functions
        self.update_params()

    def update_params(self, quiet=False):
        '''
        Creates an Imager and list of Blades and initializes them based on User Defined Params
        '''
        #Instantiate Blades with radial symmetry
        for i,n in enumerate(range(self.nblades)):
            B = Blade(nleds=self.nleds, ini_angle=i*360//self.nblades)
            B.hz = self.freq
            B.update_params(quiet=True)
            self.blade_list.append(B)
        
        #Load Image
        try:
            self.img = cv.imread(self.img_path, cv.IMREAD_COLOR)
            self.img = self.img[:,:,::-1] #cv reads vals as BGR so change to RGB
        except:
            print('Invalid Img Path')
        
        #Instantiate Imager
        self.imager = Imager(self.img, self.blade_list[0], mode=self.mode)

        if not quiet:
            print('Fan Parameters Updated')
    
    
    def update_led_vals(self, blade:Blade, cur_t):
        '''
        Function that updates LED RGB values on blade based on current time
        '''
        #Reset Values
        blade.reset_cur_vals()

        #Get indices
        posx, posy = blade.update_pos(cur_t)
        imgx, imgy = self.imager.pos2img(posx,posy)
        
        #Remove image indices out of range
        cx = np.logical_and(0 <= imgx, imgx < self.imager.img_xres)
        cy = np.logical_and(0 <= imgy, imgy < self.imager.img_yres)
        cix = np.logical_and(cx, cy)

        imgx = imgx[cix]
        imgy = imgy[cix]

        blade.cur_vals[cix] = self.img[imgy,imgx]
    
    ##------------------- DEBUG FUNCTIONS -------------------------------------------------------------------------------------------------------------------##
    def run_sim(self, interval=.0001, title='', ax:Axes=None, marker_size=1):
        '''
        Using currently defined params, plots position of each blade LED over one full rotation

        interval: Determines how often to plot LED position (independent of frequency), time for 1 rotation = 1/freq, so interval 
        should be smaller than that

        title: If provided, adds title to top of plot

        ax: If a subplot ax is provided, will plot on that ax

        marker_size: Changes size of point being plotted
        '''
        if interval > 1/self.freq:
            raise ValueError(f'Plotting interval should be less than current rotation time: {np.round(1/self.freq,4)} s')
        
        cur_t = 0
        while cur_t < 1/self.freq:
            for b in self.blade_list:
                self.update_led_vals(b, cur_t)
                if ax is not None:
                    ax.scatter(b.cur_x, b.cur_y, c=b.cur_vals/255, s=marker_size) #c only takes vals [0-1]
                else:
                    plt.scatter(b.cur_x, b.cur_y, c=b.cur_vals/255, s=marker_size) #c only takes vals [0-1]

            cur_t += interval
        
        if ax is not None:
            title_out = title
            ax.set_xlim([-1*b.led_list.max(), b.led_list.max()])
            ax.set_ylim([-1*b.led_list.max(), b.led_list.max()])
            ax.set_title(title_out)
            ax.set_box_aspect(1)
        else:
            title_out = [f'1 Rotation - {title}' if len(title) > 0 else '1 Rotation']
            plt.xlim([-1*b.led_list.max(), b.led_list.max()])
            plt.ylim([-1*b.led_list.max(), b.led_list.max()])
            plt.title(title_out[0])
            plt.show()
    
    def get_avg_time(self, run_time=5):
        '''
        Returns list of delta times per loop of processing, theoretical fastest time we can update LEDs while still being in sync

        run_time: How long (s) to run and acquire loop times
        '''
        times = []
        cur_t = 0
        while cur_t < run_time:
            start_time = time.perf_counter()
            for b in self.blade_list:
                self.update_led_vals(b, cur_t)
            deltatime = time.perf_counter() - start_time
            times.append(deltatime)
            cur_t += deltatime
        
        times = np.array(times)
        return times

##Debug
if __name__ == '__main__':
    img_path = '.debug/images/asa_my_beloved.jpg'
    # img_path = '.debug/images/space_square.jpg'
    
    F = Fan(nleds=50, nblades=2, freq=24, img_path=img_path, mode='circum_tb')
    F.run_sim()
    # times = F.get_avg_time()
    print('Done')