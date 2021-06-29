#!/usr/bin/env python
# coding: utf-8

# In[218]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
        
class Fan:
    '''Creates instance of a Fan blade with a strip of LEDs.'''
    def __init__(self, num=10, spacing=1, freq=60):
        self.leds_num = num #Number of LEDs
        self.leds_spacing = spacing #Centimeters
        self.freq = freq #Hertz (spins/sec)
        
        self.x_values = []
        self.y_values = []
        self.matrix = [] #LED layout
        
        self.create_matrix()
    
    class Animation:
        '''Inner Class specifically to animate LEDs in motion for reference.'''
        def __init__(self, x, y, spacing, freq):
            self.x, self.y = x, y
            self.leds_spacing, self.freq = spacing, freq
            self.fig = plt.Figure()
            self.ax = self.fig.add_subplot(111)
            self.line, = self.ax.plot(self.x[0], self.y[0], 'ro') #Representing LEDS as red dots, no color data rn
            
        def update_anim(self, i):
            '''Iterates through frames of the data.'''
            self.line.set_xdata(self.x[i])
            self.line.set_ydata(self.y[i])
            return line,
        
        def anim_func(self):
            '''Tkinter GUI.'''
            lim = np.abs(self.x.max())
            xmin, ymin = -1*lim, -1*lim
            xmax, ymax = lim, lim
            
            root = tk.Tk()
            
            label = tk.Label(root,text="Fan Simulation").grid(column=0, row=0)
            
            canvas = FigureCanvasTkAgg(self.fig, master=root)
            canvas.get_tk_widget().grid(column=0,row=1)
            
            self.ax.set_xlim([xmin-self.leds_spacing, xmax+self.leds_spacing])
            self.ax.set_ylim([ymin-self.leds_spacing, ymax+self.leds_spacing])
            ani = animation.FuncAnimation(
                self.fig, self.update_anim,
                self.freq, interval=120, blit=False
            ) #interval is delay between frames, should be changed later
            
            tk.mainloop()
        
    def set_num(self, num):
        '''Sets the number of LEDs on a strip.'''
        if num >= 1:
            self.leds_num = num
        else:
            raise ValueError('Please choose an appropriate integer value greater or equal to 1.')
    
    def set_spacing(self, spacing):
        '''Sets spacing between LEDs on a strip'''
        if spacing > 0:
            self.leds_spacing = spacing
        else:
            raise ValueError('Please choose an appropriate spacing value greater than 0.')
    
    def set_freq(self, freq):
        '''Sets the frequency of rotation for a fan. Positive values are CCW rotation, negative are CW.'''
        self.freq = freq
    
    def create_matrix(self):
        '''Creates a matrix using numpy arrays to assign pixel coordinates
        to the fan based on its defined features.'''
        r_values = []
        for led in range(self.leds_num):
            r_values.append((led+1) * self.leds_spacing)
        r_values = np.array(r_values) #Position of each LED along axis
        
        x_values = []
        y_values = []
        
        matrix = [] #Will be of the form matrix[time_i[led_i]]
        for t_i in range(self.freq): #Each instant when data is updated, time_i
            led_list = []
            x_list = []
            y_list = []
            for led_i in range(self.leds_num): #For each LED, led_i
                for r in r_values:
                    x = r*np.cos((2*np.pi / self.freq) * t_i) #Should actually be the fps of video file
                    y = r*np.sin((2*np.pi / self.freq) * t_i) #Using freq so we can see motion clearly
                    
                    x_list.append(x)
                    y_list.append(y)
                    led_list.append(np.array([x,y]))
            matrix.append(np.array(led_list))
            x_values.append(np.array(x_list))
            y_values.append(np.array(y_list))
        
        self.x_values = np.array(x_values)
        self.y_values = np.array(y_values)
        self.matrix = np.array(matrix)
    
    def get_matrix(self):
        '''Returns matrix.'''
        return self.matrix
    
    def get_xy(self):
        '''Returns x values and y values arrays as (x,y).'''
        return (self.x_values, self.y_values)
    
    def animate(self):
        '''Creates an animation showing current setup of LEDs.'''
        x, y = self.get_xy()
        self.Animation(x, y, self.leds_spacing, self.freq).anim_func()
        


# In[224]:


#Demo Function
def main():
    num = int(input("Number of LEDs? "))
    spacing = float(input("Spacing between LEDs in cm? "))
    freq = int(input("Freq in Hz? "))
    
    f = Fan(num, spacing, freq) #Instantiate a Fan
    f.animate() #Animate Fan

main()


# In[ ]:




