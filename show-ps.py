#!/usr/bin/env python3

import math
import time

# import random                    # Required for random values
# from colorsys import hsv_to_rgb  # required for trippy bar colours

import psutil

import unicornhathd


print("""Unicorn HAT HD: ps

This provides a visual display of process info.

Press Ctrl+C to exit!

""")

unicornhathd.rotation(90)
unicornhathd.brightness(0.6)
u_width, u_height = unicornhathd.get_shape()

bar_speed = 4
bar_width = 2


max_bar_height = u_height * 3 / 4 


def get_color_by_proc_info(pinfo):
    # Default
    r = 255
    g = 128
    b = 0
    
    if pinfo['username'] == 'pi':
        r = 0
        g = 128
        b = 64    

    if pinfo['username'] == 'root':
        r = 255
        g = 0
        b = 0

    if pinfo['status'] == psutil.STATUS_RUNNING:
        r = 0
        g = 255
        b = 0        
        
    return r,g,b
    
# Create our array of values to display on the chart
# These should always be scaled to the range 0.0 to 1.0

# Sine wave!
values = [(math.sin((x / 16.0) * math.pi) + 1.0) / 2.0 for x in range(32)]

# Random values
# values = [random.randint(0,127) / 127.0 for _ in range(32)]

try:
    while True:
        y = 0
        x = 0
        for proc in psutil.process_iter():
            pinfo = proc.as_dict(['pid', 'name', 'username', 'status'])
            print(pinfo)
            if y > max_bar_height:
                y = 0
                x += 1
            if x > u_width:
                break
            redval, greenval, blueval = get_color_by_proc_info(pinfo)
            unicornhathd.set_pixel(x, y, redval, greenval, blueval)
            y += 1
        while x < u_width:
            if y > max_bar_height:
                y = 0
                x += 1
            if x > u_width:
                break
            #unicornhathd.set_pixel(x, y, 0, 0, 0)
            y += 1

        unicornhathd.show()
        time.sleep(1.0 / bar_speed)

except KeyboardInterrupt:
    unicornhathd.off()
