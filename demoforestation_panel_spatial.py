# This script runs expanded econometric models using both old and new data

# Import required modules

import pandas as pd
import numpy as np
import statsmodels.api as stats
from ToTeX import restab

# Reading in the data

data = pd.read_csv('C:/Users/User/Documents/Data/demoforestation_panel_spatial.csv', encoding = 'cp1252')
W = pd.read_csv('C:/Users/User/Documents/Data/demoforestation_W.csv', header = None)

# Create spatially democracy term for neighbors

W2 = np.zeros((len(W)*2,len(W)*2))
W2[0:len(W),0:len(W)] = W
W2[len(W):2*len(W),len(W):2*len(W)] = W

Dp = np.dot(W2,data.Democracy)
D2p = np.dot(W2,data.Democracy_2)

# Add these to the data sets

data = pd.concat([data, pd.DataFrame(Dp, columns = ['W*Demo']), pd.DataFrame(D2p, columns = ['W*Demo_2'])], axis = 1)

# Data prep

df1 = data[['Rate', 'W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent']].dropna()
df2 = data[['Rate', 'W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']].dropna()
df3 = data[['Rate', 'W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent', '2010']].dropna()
df4 = data[['Rate', 'W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent']].dropna()
df5 = data[['Rate', 'W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']].dropna()
df6 = data[['Rate', 'W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent', '2010']].dropna()

d1 = pd.get_dummies(df1['Continent'])
d3 = pd.get_dummies(df3['Continent'])
d4 = pd.get_dummies(df4['Continent'])
d6 = pd.get_dummies(df6['Continent'])

X1 = stats.add_constant(df1[['W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land']])
X2 = stats.add_constant(df2[['W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']])
X3 = stats.add_constant(df3[['W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']])
X4 = stats.add_constant(df4[['W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate']])
X5 = stats.add_constant(df5[['W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']])
X6 = stats.add_constant(df6[['W*Demo', 'W*Demo_2', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']])

X1 = X1.join(d1).drop('Oceania', axis = 1)
X3 = X3.join(d3).drop('Oceania', axis = 1)
X4 = X4.join(d4).drop('Oceania', axis = 1)
X6 = X6.join(d6).drop('Oceania', axis = 1)

# Running regressions and saving results

Ys = [df1['Rate'], df2['Rate'], df3['Rate'], df4['Rate'], df5['Rate'], df6['Rate']]
Xs = [X1, X2, X3, X4, X5, X6]
res_list = []

for i in range(len(Xs)):

    res = stats.OLS(Ys[i],Xs[i]).fit()
    res_list.append(res)
    print(res.summary())
    file = open('C:/Users/User/Documents/Data/Demoforestation/Spatial/Panel_Model_' + str(i+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/Demoforestation/Spatial/restab_panel.txt')

# Create binary indicator for whether or not a nation's neighbors were, on average, more democratic

bi = [1 if (data['W*Demo'][i] > data['Democracy'][i]) else 0 for i in range(len(data))]
data = pd.concat([data, pd.DataFrame(bi, columns = ['W*D>D'])], axis = 1)

# Run second set of regressions with binary indicator

# Data prep

df11 = data[['Rate', 'W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent']].dropna()
df12 = data[['Rate', 'W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']].dropna()
df13 = data[['Rate', 'W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent', '2010']].dropna()
df14 = data[['Rate', 'W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent']].dropna()
df15 = data[['Rate', 'W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']].dropna()
df16 = data[['Rate', 'W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent', '2010']].dropna()

d11 = pd.get_dummies(df11['Continent'])
d13 = pd.get_dummies(df13['Continent'])
d14 = pd.get_dummies(df14['Continent'])
d16 = pd.get_dummies(df16['Continent'])

X11 = stats.add_constant(df11[['W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land']])
X12 = stats.add_constant(df12[['W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']])
X13 = stats.add_constant(df13[['W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']])
X14 = stats.add_constant(df14[['W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate']])
X15 = stats.add_constant(df15[['W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']])
X16 = stats.add_constant(df16[['W*D>D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']])

X11 = X11.join(d11).drop('Oceania', axis = 1)
X13 = X13.join(d13).drop('Oceania', axis = 1)
X14 = X14.join(d14).drop('Oceania', axis = 1)
X16 = X16.join(d16).drop('Oceania', axis = 1)

# Running regressions and saving results

Ys = [df11['Rate'], df12['Rate'], df13['Rate'], df14['Rate'], df15['Rate'], df16['Rate']]
Xs = [X11, X12, X13, X14, X15, X16]
res_list = []

for i in range(len(Xs)):

    res = stats.OLS(Ys[i],Xs[i]).fit()
    res_list.append(res)
    print(res.summary())
    file = open('C:/Users/User/Documents/Data/Demoforestation/Spatial/Panel_Model_Binary_' + str(i+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/Demoforestation/Spatial/restab_panel_binary.txt')

# Create nonbinary indicator for whether or not a nation's neighbors were, on average, more democratic

nbi = [data['W*Demo'][i] - data['Democracy'][i] for i in range(len(data))]
data = pd.concat([data, pd.DataFrame(nbi, columns = ['W*D-D'])], axis = 1)

# Run third set of regressions with nonbinary indicator

# Data prep

df21 = data[['Rate', 'W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent']].dropna()
df22 = data[['Rate', 'W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']].dropna()
df23 = data[['Rate', 'W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent', '2010']].dropna()
df24 = data[['Rate', 'W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent']].dropna()
df25 = data[['Rate', 'W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']].dropna()
df26 = data[['Rate', 'W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent', '2010']].dropna()

d21 = pd.get_dummies(df21['Continent'])
d23 = pd.get_dummies(df23['Continent'])
d24 = pd.get_dummies(df24['Continent'])
d26 = pd.get_dummies(df26['Continent'])

X21 = stats.add_constant(df21[['W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land']])
X22 = stats.add_constant(df22[['W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']])
X23 = stats.add_constant(df23[['W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']])
X24 = stats.add_constant(df24[['W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate']])
X25 = stats.add_constant(df25[['W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']])
X26 = stats.add_constant(df26[['W*D-D', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']])

X21 = X21.join(d21).drop('Oceania', axis = 1)
X23 = X23.join(d23).drop('Oceania', axis = 1)
X24 = X24.join(d24).drop('Oceania', axis = 1)
X26 = X26.join(d26).drop('Oceania', axis = 1)

# Running regressions and saving results

Ys = [df21['Rate'], df22['Rate'], df23['Rate'], df24['Rate'], df25['Rate'], df26['Rate']]
Xs = [X21, X22, X23, X24, X25, X26]
res_list = []

for i in range(len(Xs)):

    res = stats.OLS(Ys[i],Xs[i]).fit()
    res_list.append(res)
    print(res.summary())
    file = open('C:/Users/User/Documents/Data/Demoforestation/Spatial/Panel_Model_NonBinary_' + str(i+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/Demoforestation/Spatial/restab_panel_nonbinary.txt')

