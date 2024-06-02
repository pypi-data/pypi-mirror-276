# -*- coding: utf-8 -*-
"""
@author: Noemi E. Cazzaniga - 2024
@email: noemi.cazzaniga@polimi.it
"""

from faostat.faostat import get_data, get_data_df,\
                              get_par, get_par_df,\
                              get_requests_args,\
                              list_datasets, list_datasets_df,\
                              list_pars, list_pars_df,\
                              set_requests_args,\
                              get_areas, get_years, get_elements, get_items

__all__ = ['get_data', 'get_data_df',\
           'get_par', 'get_par_df', 'get_requests_args',\
           'list_datasets', 'list_datasets_df',\
           'list_pars', 'list_pars_df', 'set_requests_args',\
           'get_areas', 'get_years', 'get_elements', 'get_items']
