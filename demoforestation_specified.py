# This script runs expanded econometric models using both old and new data

# Import required modules

import pandas as pd
import statsmodels.api as stats
from ToTeX import restab

# Reading in the data

data = pd.read_csv('C:/Users/User/Documents/Data/demoforestation_panel.csv')

# Data prep

df1 = data[['Rate', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent']].dropna()
df2 = data[['Rate', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']].dropna()
df3 = data[['Rate', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Continent', '2010']].dropna()
df4 = data[['Rate', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent']].dropna()
df5 = data[['Rate', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']].dropna()
df6 = data[['Rate', 'Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', 'Continent', '2010']].dropna()

d1 = pd.get_dummies(df1['Continent'])
d3 = pd.get_dummies(df3['Continent'])
d4 = pd.get_dummies(df4['Continent'])
d6 = pd.get_dummies(df6['Continent'])

X1 = stats.add_constant(df1[['Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land']])
X2 = stats.add_constant(df2[['Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']])
X3 = stats.add_constant(df3[['Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', '2010']])
X4 = stats.add_constant(df4[['Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate']])
X5 = stats.add_constant(df5[['Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']])
X6 = stats.add_constant(df6[['Democracy', 'Democracy_2', 'Education', 'Rural_Pop', 'Ln_Land', 'Ag_Land_Rate', '2010']])

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
    file = open('C:/Users/User/Documents/Data/Demoforestation/Specified/Panel_Model_' + str(i+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/Demoforestation/Specified/restab_panel.txt')

