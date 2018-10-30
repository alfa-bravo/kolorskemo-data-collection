#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 19:06:08 2018

@author: jennifernghinguyen
"""

import csv
from itertools import islice
from colors_harmony import *


start = 1
end = None

data_read_only = '../dataset/color_names_rgb.csv'
data_output = '../dataset/color_names_rgb_output.csv'

with open(data_read_only, "r") as file:
        csv_f = csv.reader(file)
        with open(data_output, "a", newline="") as output_file:
            for row in islice(csv_f, start, end, 1):
                # each row is a list
                #['Absolute zero', '#0048BA', '0', '72', '186']
                writer = csv.writer(output_file)
                writer.writerow(row)
                for mono_color in monochromatic(Color(list(map(int, row[2:])))):
                    mono_color[2:]= mono_color
                    mono_color[0] = row[0]
                    mono_color[1] = ('#%02x%02x%02x' % (mono_color[2], mono_color[3], mono_color[4])).upper()
                    #print(mono_color)
                    
                    
                    writer.writerow(mono_color)
                
                