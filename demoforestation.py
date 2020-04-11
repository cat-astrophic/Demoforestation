# This script will run every scipt in the demoforestation project

# Load modules for making new directories

import os

# Declare path where the Demoforestation folder will be made

filepath = 'C:/Users/User/Documents/Data/'

# Make all drectories necessary for this project

directories = ['Demoforestation', 'Demoforestation/Replication', 'Demoforestation/Specified', 'Demoforestation/Spatial']

for d in directories:
    
    try:
        
        os.mkdir(filepath + d)
    
    except:
        
        continue

# Load the scripts

import demoforestation_replication as first # replication study
import demoforestation_new_data as second # repeat above with new data
import demoforestation_specified as third # panel data analysis
import demoforestation_differenced as fourth # differenced data analysis
import demoforestation_specified_spatial as fifth # spatial democracy term included
import demoforestation_differenced_spatial as sixth # spatial democracy term included

# Run them

first
second
third
fourth
fifth
sixth

