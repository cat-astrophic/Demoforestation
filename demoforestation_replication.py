# This script does the replication of [B&M 2011] component of the demoforestation paper

# Import required modules

import numpy as np
import pandas as pd
import statsmodels.api as stats
from matplotlib import pyplot as plt

# Reading in the data

data = pd.read_csv('C:/Users/User/Documents/Data/demoforestation.csv')

# (1) Replicating Figure 1

# Structuring dataframes

Yf1 = data['Rate_9000']

Xf11 = stats.add_constant(data['Democracy(20)_90'])
Xf12 = stats.add_constant(data[['Democracy(20)_90', 'Democracy(20)_90_2']])

f1m1 = stats.OLS(Yf1,Xf11)
f1m2 = stats.OLS(Yf1,Xf12)

f1r1 = f1m1.fit()
print(f1r1.summary())
file = open('C:/Users/User/Documents/Data/Demoforestation/Replication/Figure_1_model_1.txt', 'w')
file.write(f1r1.summary().as_text())
file.close()

f1r2 = f1m2.fit()
print(f1r2.summary())
file = open('C:/Users/User/Documents/Data/Demoforestation/Replication/Figure_1_model_2.txt', 'w')
file.write(f1r2.summary().as_text())
file.close()

# Recreating the plot

plt.figure()
plt.scatter(data['Democracy(20)_90'], data['Rate_9000'], s = 40)
plt.xlabel('Democracy Index')
plt.ylabel('Deforestation Rate')
plt.ylim(-15.5,10.5)
plt.xlim(-10.5,10.5)
basis = [i/10 for i in range(-120,121)]
l1 = [0.0741 + 0.0041*(i/10) for i in range(-120,121)]
l2 = [0.9628 + 0.0480*(i/10) - 0.0220*(i/10)**2 for i in range(-120,121)]
plt.plot(basis, l1, 'k-', linewidth = 4)
plt.plot(basis, l2, 'r-', linewidth = 4)
plt.savefig('C:/Users/User/Documents/Data/Demoforestation/Replication/Figure_1.eps')

# (2) Replicating the 7 regression models

df1 = data[['Rate_9000', 'Democracy(20)_90', 'Democracy(20)_90_2']].dropna()
df2 = data[['Rate_9000', 'Democracy(20)_90', 'Democracy(20)_90_2', 'Education_90', 'Rural_Population_90', 'Ln_Land', 'CCI_90']].dropna()
df3 = data[['Rate_9000', 'Democracy(20)_90', 'Democracy(20)_90_2', 'Education_90', 'Rural_Population_90', 'Ln_Land']].dropna()
df4 = data[['Rate_9000', 'Democracy(20)_90', 'Democracy(20)_90_2', 'Education_90', 'Rural_Population_90', 'Ln_Land', 'GDP_cap_90']].dropna()
df5 = data[['Rate_9000', 'Democracy(20)_90', 'Democracy(20)_90_2', 'Education_90', 'Rural_Population_90', 'Ln_Land', 'GDP_cap_90', 'GDP_cap_90_2']].dropna()
df6 = data[['Rate_9000', 'Education_90', 'Rural_Population_90', 'Ln_Land', 'GDP_cap_90', 'GDP_cap_90_2']].dropna()
df7 = data[['Rate_9000', 'GDP_cap_90', 'GDP_cap_90_2']].dropna()

X1 = stats.add_constant(df1[['Democracy(20)_90', 'Democracy(20)_90_2']])
X2 = stats.add_constant(df2[['Democracy(20)_90', 'Democracy(20)_90_2', 'Education_90', 'Rural_Population_90', 'Ln_Land', 'CCI_90']])
X3 = stats.add_constant(df3[['Democracy(20)_90', 'Democracy(20)_90_2', 'Education_90', 'Rural_Population_90', 'Ln_Land']])
X4 = stats.add_constant(df4[['Democracy(20)_90', 'Democracy(20)_90_2', 'Education_90', 'Rural_Population_90', 'Ln_Land', 'GDP_cap_90']])
X5 = stats.add_constant(df5[['Democracy(20)_90', 'Democracy(20)_90_2', 'Education_90', 'Rural_Population_90', 'Ln_Land', 'GDP_cap_90', 'GDP_cap_90_2']])
X6 = stats.add_constant(df6[['Education_90', 'Rural_Population_90', 'Ln_Land', 'GDP_cap_90', 'GDP_cap_90_2']])
X7 = stats.add_constant(df7[['GDP_cap_90', 'GDP_cap_90_2']])

mod1 = stats.OLS(df1['Rate_9000'],X1)
mod2 = stats.OLS(df2['Rate_9000'],X2)
mod3 = stats.OLS(df3['Rate_9000'],X3)
mod4 = stats.OLS(df4['Rate_9000'],X4)
mod5 = stats.OLS(df5['Rate_9000'],X5)
mod6 = stats.OLS(df6['Rate_9000'],X6)
mod7 = stats.OLS(df7['Rate_9000'],X7)

mods = [mod1, mod2, mod3, mod4, mod5, mod6, mod7]

for mod in mods:
    
    res = mod.fit()
    print(res.summary())
    file = open('C:/Users/User/Documents/Data/Demoforestation/Replication/Model_' + str(mods.index(mod)+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

# (3) Replicating the cluster analyses

# Recreate the statistics in Table (3) in the original paper

# Record group level statistics

Type6 = pd.DataFrame(np.zeros((2,6)), columns = data.Type6.unique(), index = ['Democracy', 'Rate_9000'])
Type3 = pd.DataFrame(np.zeros((2,3)), columns = data.Type3.unique(), index = ['Democracy', 'Rate_9000'])

for c in Type6.columns:
    
    df = data[data['Type6'] == c]
    Type6[c]['Democracy'] = np.mean(df['Democracy(20)_90'])
    Type6[c]['Rate_9000'] = np.mean(df['Rate_9000'])

for c in Type3.columns:
    
    df = data[data['Type3'] == c]
    Type3[c]['Democracy'] = np.mean(df['Democracy(20)_90'])
    Type3[c]['Rate_9000'] = np.mean(df['Rate_9000'])

# Create scatter plots from these data frames

Type6labs = ['DEM-W', 'AR', 'DEM-S', 'TM', 'RDP', 'TOT']
plt.figure()
plt.scatter(Type6.iloc[0], Type6.iloc[1], c = 'k', s = 60)
v = [4,0,4,1.5,2,-1]

for idx, lab in enumerate(Type6labs):
    
    plt.annotate(lab, (Type6.iloc[0][idx]-.25*v[idx], Type6.iloc[1][idx]-.5))

plt.xlabel('Democracy Index')
plt.ylabel('Deforestation Rate')
Type6b = Type6[['Traditional Monarchy', 'Totalitarian Regime', 'Authoritarian', 'Restricted Democratic Practice', 'Weak Democracy', 'Strong Democracy']]
plt.plot(Type6b.iloc[0], Type6b.iloc[1], 'k--')
plt.xlim(-9.5,10.5)
plt.ylim(-4.7,1.8)
plt.savefig('C:/Users/User/Documents/Data/Demoforestation/Replication/Figure_2a.eps')

plt.figure()
plt.scatter(Type3.iloc[0], Type3.iloc[1], c = 'k', s = 60)

for idx, lab in enumerate(Type3.columns):
    
    plt.annotate(lab, (Type3.iloc[0][idx]-.4, Type3.iloc[1][idx]-.067))

plt.xlabel('Democracy Index')
plt.ylabel('Deforestation Rate')
l3a = [0.46939 + 0.02778*(i/100) - 0.01203*(i/100)**2 for i in range(-625,35)]
l3b = [0.47038 - 0.00821*(i/100)**2 for i in range(35,833)]
plt.plot([(i/100) for i in range(-625,35)], l3a, 'k--')
plt.plot([(i/100) for i in range(35,833)], l3b, 'k--')
plt.xlim(-7.25,9.25)
plt.ylim(-0.3,0.55)
plt.savefig('C:/Users/User/Documents/Data/Demoforestation/Replication/Figure_2b.eps')

