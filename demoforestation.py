# This script will run every scipt in the demoforestation project

# Load modules for making new directories

import os

# Declare path where the Demoforestation folder will be made
# You need to manually update /User/ to your username
# This will need to be done in all called scripts...sorry

filepath = 'C:/Users/User/Documents/Data/'

# Make all drectories necessary for this project

directories = ['Demoforestation', 'Demoforestation/Replication', 'Demoforestation/Specified', 'Demoforestation/Spatial']

for d in directories:
    
    try:
        
        os.mkdir(filepath + d)
    
    except:
        
        continue

# Running the main models

# Load the scripts

import demoforestation_replication as first # replication study
import demoforestation_new_data as second # repeat above with new data
import demoforestation_specified as third # panel data analysis
import demoforestation_differenced as fourth # differenced data analysis
import demoforestation_panel_spatial as fifth # spatial democracy term included
import demoforestation_differenced_spatial as sixth # spatial democracy term included

import demoforestation_specified_ROB as third_rob # panel data analysis with democracy and urbanization
import demoforestation_differenced_ROB as fourth_rob # differenced data analysis with democracy and urbanization
import demoforestation_panel_spatial_ROB as fifth_rob # spatial democracy term included
import demoforestation_differenced_spatial_ROB as sixth_rob # spatial democracy term included

import demoforestation_specified_ROB2 as third_rob2 # panel data analysis with urbanization in place of democracy
import demoforestation_differenced_ROB2 as fourth_rob2 # differenced data analysis with urbanization in place of democracy
import demoforestation_panel_spatial_ROB2 as fifth_rob2 # spatial democracy term included
import demoforestation_differenced_spatial_ROB2 as sixth_rob2 # spatial democracy term included

# Run them

first
second
third
fourth
fifth
sixth

third_rob
fourth_rob
fifth_rob
sixth_rob

third_rob2
fourth_rob2
fifth_rob2
sixth_rob2

