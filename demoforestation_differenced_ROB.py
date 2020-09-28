# This script runs expanded econometric models using both old and new data - ROBUST

# Import required modules

import pandas as pd
import statsmodels.api as stats
from ToTeX import restab

# Reading in the data

data = pd.read_csv('C:/Users/User/Documents/Data/demoforestation_differenced.csv')

# Add Urbanization squared to the data for the robustness checks

U = pd.Series(data.Urbanization*data.Urbanization, name = 'Urbanization_2')
data = pd.concat([data, U], axis = 1)

# Data prep

dXi = data['Democracy']*data['GDP_per_capita']
data = pd.concat([data, pd.DataFrame(dXi, columns = ['D X GDP'])], axis = 1)

df1 = data[['Rate', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Continent']].dropna()
df2 = data[['Rate', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate', 'Continent']].dropna()
df3 = data[['Rate', 'Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate', 'Tariff_Rate', 'Continent']].dropna()

d1 = pd.get_dummies(df1['Continent'])
d2 = pd.get_dummies(df2['Continent'])
d3 = pd.get_dummies(df3['Continent'])

X1 = stats.add_constant(df1[['Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP']])
X2 = stats.add_constant(df2[['Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate']])
X3 = stats.add_constant(df3[['Democracy', 'Democracy_2', 'Urbanization', 'Urbanization_2', 'Education', 'Rural_Pop', 'Ln_Land', 'GDP_per_capita', 'D X GDP', 'Ag_Land_Rate', 'Tariff_Rate']])

X4 = X1.join(d1).drop('Oceania', axis = 1)
X5 = X2.join(d2).drop('Oceania', axis = 1)
X6 = X3.join(d3).drop('Oceania', axis = 1)

# Running regressions and saving results

Ys = [df1['Rate'], df2['Rate'], df3['Rate'], df1['Rate'], df2['Rate'], df3['Rate']]
Xs = [X1, X2, X3, X4, X5, X6]
res_list = []

for i in range(len(Xs)):

    res = stats.OLS(Ys[i],Xs[i]).fit(cov_type = 'HC1')
    res_list.append(res)
    print(res.summary())
    file = open('C:/Users/User/Documents/Data/Demoforestation/Specified/Differenced_Model_ROB_' + str(i+1) + '.txt', 'w')
    file.write(res.summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/Demoforestation/Specified/restab_differenced_ROB.txt')

