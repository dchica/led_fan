import numpy as np

def rads(deg):
    '''
    Helper function to convert Degrees into Radians
    '''
    return deg*(2*np.pi/360)
    
def degs(rad):
    '''
    Helper function to convert Radians into Degrees
    '''
    return rad*(360/(2*np.pi))