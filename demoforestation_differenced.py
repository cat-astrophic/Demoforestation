# This script runs expanded econometric models using both old and new data

# Import required modules

import pandas as pd
import statsmodels.api as stats
from matplotlib import pyplot as plt
import numpy as np
from ToTeX import restab

# Reading in the data

data = pd.read_csv('C:/Users/User/Documents/Data/demoforestation_differenced.csv')

# Data prep

df1 = data[['Rate', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent']].dropna()
df2 = data[['Rate', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent']].dropna()
df3 = data[['Rate', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Tariff_Rate', 'Continent']].dropna()

d1 = pd.get_dummies(df1['Continent'])
d2 = pd.get_dummies(df2['Continent'])
d3 = pd.get_dummies(df3['Continent'])

X1 = stats.add_constant(df1[['Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land']])
X2 = stats.add_constant(df2[['Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate']])
X3 = stats.add_constant(df3[['Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Tariff_Rate']])

X1 = X1.join(d1).drop('Oceania', axis = 1)
X2 = X2.join(d2).drop('Oceania', axis = 1)
X3 = X3.join(d3).drop('Oceania', axis = 1)

# Running regressions and saving results

Ys = [df1['Rate'], df2['Rate'], df3['Rate']]
Xs = [X1, X2, X3]
res_list = []

for i in range(len(Xs)):

    res = stats.OLS(Ys[i],Xs[i]).fit()
    res_list.append(res)
    print(res.summary())
    file = open('C:/Users/User/Documents/Data/Demoforestation/Specified/Differenced_Model_' + str(i+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/Demoforestation/Specified/restab_differenced.txt')

# Creating plots

# (1) Scatter plot with democracy trend line

plt.scatter(data['Democracy'],data['Rate'])
l = [.3819 - .1186*(i/100) for i in range(-700,900)]
basis = [i/100 for i in range(-700,900)]
plt.plot(basis, l, 'k-', linewidth = 4)
plt.xlabel('Change in Democracy Index')
plt.ylabel('Change in Deforestation Rate')
plt.savefig('C:/Users/User/Documents/Data/Demoforestation/Specified/Figure_A.eps')

# Record group level statistics

Type6 = pd.DataFrame(np.zeros((2,6)), columns = data.Type6.unique(), index = ['Democracy', 'Rate'])
Type3 = pd.DataFrame(np.zeros((2,3)), columns = data.Type3.unique(), index = ['Democracy', 'Rate'])

for c in Type6.columns:
    
    df = data[data['Type6'] == c]
    Type6[c]['Democracy'] = np.mean(df['Democracy'])
    Type6[c]['Rate'] = np.mean(df['Rate'])

for c in Type3.columns:
    
    df = data[data['Type3'] == c]
    Type3[c]['Democracy'] = np.mean(df['Democracy'])
    Type3[c]['Rate'] = np.mean(df['Rate'])

# Create scatter plots from these data frames

Type6labs = ['DEM-W', 'AR', 'DEM-S', 'TM', 'RDP', 'TOT']
plt.figure()
plt.scatter(Type6.iloc[0], Type6.iloc[1], c = 'k', s = 60)
vx = [1.5,.8,1.5,.8,1,1]
vy = [0,0,-.6,0,1,.9]

for idx, lab in enumerate(Type6labs):
    
    plt.annotate(lab, (Type6.iloc[0][idx]-.5*vx[idx], Type6.iloc[1][idx]-.5*vy[idx]))

plt.xlabel('Change in Democracy Index')
plt.ylabel('Change in Deforestation Rate')
plt.xlim(-1.5,4)
plt.ylim(-1.5,4)
plt.savefig('C:/Users/User/Documents/Data/Demoforestation/Specified/Figure_B.eps')

plt.figure()
plt.scatter(Type3.iloc[0], Type3.iloc[1], c = 'k', s = 60)
vx = [.4,.5,-.3]
vy = [.02,0,.02]

for idx, lab in enumerate(Type3.columns):
    
    plt.annotate(lab, (Type3.iloc[0][idx]-vx[idx], Type3.iloc[1][idx]-vy[idx]))

plt.xlabel('Change in Democracy Index')
plt.ylabel('Change in Deforestation Rate')
plt.ylim(0,0.35)
plt.savefig('C:/Users/User/Documents/Data/Demoforestation/Replication/Figure_C.eps')

