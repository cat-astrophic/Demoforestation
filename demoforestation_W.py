# Script to manually create a custom spatial weight matrix for a panel data set

# Import required modules

import numpy as np
import pandas as pd

# Declare filepaths to read and write to

filepath = 'C:/Users/User/Documents/Data/demoforestation.csv' # Your panel data
spatial_data = 'C:/Users/User/Documents/Data/demoforestation_spatial.csv' # Output path for data w/o islands
W_ref = 'C:/Users/User/Documents/Data/demoforestation_W_reference.csv' # Initial output from the manual process
output = 'C:/Users/User/Documents/Data/demoforestation_W.csv' # Final spatial weights matrix

# Read the data into a dataframe

data = pd.read_csv(filepath)

# Create a list of unique entries for all nations using the Country dataseries

nations = data.Country.unique()

# Create the binary spatial weight matrix W

W = np.zeros([len(nations),len(nations)])

for nation in nations:
    
    idx = np.where(nations == nation)[0][0]
    print(nation)
    accepted = False
    
    while accepted != True: # Ensures that input is an integer
        
        try:
            
            adjacencies = int(input('How many adjacencies? '))
            accepted = True
            
        except:
            
            continue
        
    for i in range(adjacencies):
        
        complete = False
        
        while complete == False:
            
            try: # Ensures that the input is a viable match, else repeat entry
                
                neighbor = input('Input next neighbor: ')
                check = np.where(nations == neighbor)[0][0]
                print(check)
                complete = True
                
            except:
                
                continue
            
        W[idx][check] = 1

# Ensure symmetry of W (in cases of inconsistencies in the munual entry process)

for i in range(len(W)):
    
    for j in range(len(W[i])):
        
        if W[i][j] > 0:
            
            W[j][i] = W[i][j]
         
# Write W to file for future reference

W = pd.DataFrame(W)
W.to_csv(W_ref, index = False, header = False)

# Create a reference indicating if the entries have neighbors for that year

ref = sum(W.values)
        
# Remove appropriate entries from full data set (those with row sum == 0 in W)

df = pd.DataFrame(columns = data.columns)

for i in range(len(ref)):
    
    if ref[i] > 0:
        
        df = pd.concat([df, data.iloc[[i]]], axis = 0)

df = df.reset_index(drop = True)

# Write new dataframe to csv

df.to_csv(spatial_data, index = False)

# Create final (binary) spatial weights matrix

SW = np.zeros((len(df.Country),len(df.Country)))

for i in range(len(df.Country)):
    
    id1 = np.where(nations == df.Country[i])[0][0]
    
    for j in range(len(df.Country)):
        
        id2 = np.where(nations == df.Country[j])[0][0]
        SW[i,j] = W[id1][id2]

# Normalize the spatial weights matrix and write it to file

for i in range(len(SW)):
    
    s = sum(SW[i,:])
    SW[i,:] = SW[i,:] / s

SW = pd.DataFrame(SW)
SW.to_csv(output, index = False, header = False)

