# -*- coding: utf-8 -*-
"""
@author: Noemi E. Cazzaniga - 2024
@email: noemi.cazzaniga@polimi.it
"""


## Examples in README.md


from faostat import *

ld = list_datasets()
print('list_datasets =')
for el in range(0,5):
	print(ld[el])

df = list_datasets_df()
print('list_datasets_df =')
for el in range(0,5):
	print(df.iloc[el,:])
    
   
pars = list_pars('QCL')
print('list_pars =')
print(pars)
    
pars_df = list_pars_df('QCL')
print('list_pars_df =')
print(pars_df)
    

a = get_par('QCL', 'area')
print('get_par =')
for el, k in enumerate(a.keys()):
	print(k, a[k])
	if el > 4:
		break

a_df = get_par_df('QCL', 'specialgroups')
print('get_par_df =')
for el in range(0,5):
	print(a_df.iloc[el,:])
    

data = get_data('QCL',pars={'element':[2312, 2313],'item':'221'})
print('get_data =')
print(data[0])
for el in range(40,45):
	print(data[el])

data_df = get_data_df('QCL',pars={'element':[2312, 2313],'item':'221'})
print('get_data_df =')
for el in range(39,44):
	print(data_df.iloc[el,:])
