import numpy as np
import cv2 as cv

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
from classes.blade import Blade

class Imager:
    '''
    Class to handle converting between a supplied Image and its corresponding Grid (LED space)

    img: Final Image to display, expect (nrows, ncols, vals_per_pix) - vals_per_pix can be 3 for RGB, 4 for RGBA, etc...
    
    blade: A Blade object to determine LED count, sizes, etc... assume all blades on Fan equal

    mode: Method to display image in fan - 'inscribe', 'circum_tb', 'circum_lr'
    '''
    def __init__(self, img, blade:Blade, mode='inscribe'):
        ##User Defined Params
        self.img = img
        self.blade = blade
        self.mode = mode

        ##Dependent Params
        self.img_xres = img.shape[1] #shape[1]: # of cols
        self.img_yres = img.shape[0] #shape[0]: # of rows
        self.max_angle = None #Only used for 'INSCRIBED'?
        self.cf_x = None #Conversion Factor x-axis
        self.cf_y = None #Conversion Factor y-axis
        
        ##Autorun Functionss
        self.update_params(quiet=True)
    
    def update_params(self, quiet=False):
        '''
        Sets per axis conversion factor based on User Defined Params
        '''
        match self.mode.upper():
            case 'INSCRIBE':
                '''
                Image fully contained in fan
                '''
                #Find angle (degrees) that results in TR position of image
                self.max_angle = degs(np.arctan(self.img_yres/self.img_xres))

                #Find TR position of LED with angle, matches image dimensions
                xl, yl = self.blade.get_pos_angle(self.max_angle, quiet=True)
                max_vx = np.max(xl)
                max_vy = np.max(yl)
                
                self.cf_x =    self.img_xres/max_vx / 2 #Divide by 2 since we work from middle of img
                self.cf_y = -1*self.img_yres/max_vy / 2 #Negative since img indexing is from TL to BR
            
            case 'CIRCUM_TB':
                '''
                Fan fully contained in image, image Top/Bot coincide with edges of fan, other sides might be out of bounds
                '''
                #Find pos at 90 degs
                _, yl = self.blade.get_pos_angle(90, quiet=True)
                max_vy = np.max(yl)
                
                #Find hyptotheical max x value
                ratio = self.img_xres/self.img_yres
                max_vx = ratio * max_vy

                self.cf_x =    self.img_xres/max_vx / 2 #Divide by 2 since we work from middle of img
                self.cf_y = -1*self.img_yres/max_vy / 2 #Negative since img indexing is from TL to BR
            
            case 'CIRCUM_LR':
                '''
                Fan fully contained in image, image Left/Right coincide with edges of fan, other sides might be out of bounds
                '''
                #Find pos at 0 degs
                xl, _ = self.blade.get_pos_angle(0, quiet=True)
                max_vx = np.max(xl)
                
                #Find hyptotheical max y value
                ratio = self.img_yres/self.img_xres
                max_vy = ratio * max_vx

                self.cf_x =    self.img_xres/max_vx / 2 #Divide by 2 since we work from middle of img
                self.cf_y = -1*self.img_yres/max_vy / 2 #Negative since img indexing is from TL to BR
        
        if not quiet:
            print('Imager Parameters Updated')
    

    def pos2img(self, x, y):
        '''
        Given x,y position in cm, returns equivalent image index xvals, yvals

        Mapping can result in values outside image bounds, that means LED should display off since out of image bounds
        '''
        # match self.mode.upper():
        #     case 'INSCRIBE':
        #         xvals = (self.cf_x * x + self.img_xres/2).astype(int)
        #         yvals = (self.cf_y * y + self.img_yres/2).astype(int)

        #         return xvals, yvals
        
        xvals = (self.cf_x * x + self.img_xres/2).astype(int)
        yvals = (self.cf_y * y + self.img_yres/2).astype(int)

        return xvals, yvals


##Debug
if __name__ == '__main__':
    B = Blade(nleds=10)
    im = cv.imread('.debug/images/space_rectangle.jpg', cv.IMREAD_COLOR)
    I = Imager(im, B, mode='inscribe')
    I.update_params()
    print('Done')