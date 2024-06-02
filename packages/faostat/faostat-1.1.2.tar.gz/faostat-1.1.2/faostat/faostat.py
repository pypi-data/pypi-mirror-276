# -*- coding: utf-8 -*-
"""
@author: Noemi E. Cazzaniga - 2024
@email: noemi.cazzaniga@polimi.it
"""


import requests
from pandas import DataFrame


__ra__ = {'timeout': 120.}
__BASE_URL__ = 'https://faostatservices.fao.org/api/v1/en/'



def set_requests_args(**kwargs):
    """
    Allows to set some arguments for "requests":
    - timeout: how long to wait for the server before raising an error. (optional)
        Default: 120 sec.
    - proxies : dict with protocol, user and password. (optional)
        For the Faostat API, only https proxy.
        Examples: {'https': 'http://myuser:mypass@123.45.67.89:1234'}
                  {'https': 'https://123.45.67.89:1234'}
        Default: None.
    - verify : for the server’s TLS certificate. (optional)
        Default: None.
    - cert : user-provided SSL certificate. (optional)
       Default: None.

    Returns
    -------
    None.

    """
    assert set(kwargs.keys()).issubset({"timeout", "proxies", "verify", "cert"}), "Wrong arguments."
    global __ra__
    for k in kwargs:
        __ra__[k] = kwargs[k]


def get_requests_args():
    """
    Get the current set arguments for "requests".
    
    Returns
    -------
    a dict with arg names and their respective values.
    """
    return __ra__


def __getresp__(url, params=None):
    """
    Makes a request and returns the response.

    Parameters
    ----------
    url : str
        URL for the request.
    params : dict, optional
        parameters to pass in URLs:
            {key: value, ...}.
        The default is None.

    Raises
    ------
    Exception
        if there is a connection problem,
        if the dataset was not found.

    Returns
    -------
    resp : response

    """
    with requests.get(url, params=params, **__ra__) as resp:
        if resp.status_code == 500 and resp.text == 'Index: 0, Size: 0':
            print("{0} not found in the Faostat server".format(url.split('?')[0].split('/')[-1]))
            raise Exception()
        if resp.status_code == 524:
            raise TimeoutError()
        resp.raise_for_status()
        # print(resp.url)
        return resp


def list_datasets(**kwargs):
    """
    Returns a list of datasets available on the Faostat server.

    Returns
    -------
    l : list
        list of available datasets and some metadata.
    **kwargs:
        https_proxy, deprecated

    """
    assert set(kwargs.keys()).issubset({'https_proxy',}), "Wrong argument."
    __depr__(**kwargs)
    
    l = [('code',
          'label',
          'date_update',
          'note_update',
          'release_current',
          'state_current',
          'year_current',
          'release_next',
          'state_next',
          'year_next'),
         ]
    response = __getresp__(__BASE_URL__ + 'groups')
    groups = [el['code'] for el in response.json()['data']]
    for group_code in groups:
        url = __BASE_URL__ + 'domains/' + group_code
        response = __getresp__(url)
        domains = response.json()['data']
        for d in domains:
            if d.get('date_update', None) is not None:
                l.append((d.get('code', None),
                          d.get('label', None),
                          d['date_update'],
                          d.get('note_update', None),
                          d.get('release_current', None),
                          d.get('state_current', None),
                          d.get('year_current', None),
                          d.get('release_next', None),
                          d.get('state_next', None),
                          d.get('year_next', None))
                          )
    return l


def list_datasets_df(**kwargs):
    """
    Returns a pandas dataframe listing the datasets available on the Faostat server.

    Returns
    -------
    l : dataframe
        list of available datasets and some metadata.
    **kwargs:
        https_proxy, deprecated

    """
    d = list_datasets(**kwargs)
    return DataFrame(d[1:], columns=d[0])


def list_pars(code, **kwargs):
    """
    Given the code of a Faostat dataset,
    returns the available parameters as list.

    Parameters
    ----------
    code : str
        code of the dataset.

    Returns
    -------
    d : list
        parameters for data filtering.
    **kwargs:
        https_proxy, deprecated

    """
    assert set(kwargs.keys()).issubset({'https_proxy',}), "Wrong argument."
    __depr__(**kwargs)

    url = __BASE_URL__ + 'dimensions/' + code
    d = [('parameter code', 'coding_systems', 'subdimensions {code: meaning}')]
    response = __getresp__(url)
    data = response.json()['data']
    for par in data:
        code = par['id']
        subdimensions = dict([(sd['id'], sd['label']) for sd in par['subdimensions']])
        coding_systems = par['subdimensions'][0]['coding_systems']  ## all the subdimensions have same coding_systems
        d.append((code, coding_systems, subdimensions))
    return d


def list_pars_df(code, **kwargs):
    """
    Given the code of a Faostat dataset,
    returns the available parameters as list.

    Parameters
    ----------
    code : str
        code of the dataset.

    Returns
    -------
    d : dataframe
        parameters for data filtering.
    **kwargs:
        https_proxy, deprecated

    """
    d = list_pars(code, **kwargs)
    return DataFrame(d[1:], columns=d[0])


def get_par(code, par, **kwargs):
    """
    Given the code of a Faostat dataset,
    and the name of one of its parameters or subdimension,
    returns the available values as dict or dataframe.

    Parameters
    ----------
    code : str
        code of the dataset.
    par : str
        code of the parameter or the subdimension.

    Returns
    -------
    d : dict
        {label: code, ...}.
    **kwargs:
        https_proxy, deprecated

    """
    assert set(kwargs.keys()).issubset({'https_proxy',}), "Wrong argument."
    __depr__(**kwargs)

    url = __BASE_URL__ + 'codes/' + par + '/' + code
    response = __getresp__(url)
    data = response.json()['data']
    d = dict()
    for el in data:
        d[el['label']] = el['code']
    return d


def get_par_df(code, par, **kwargs):
    """
    Given the code of a Faostat dataset,
    and the name of one of its parameters or subdimension,
    returns the available values as dict or dataframe.

    Parameters
    ----------
    code : str
        code of the dataset.
    par : str
        code of the parameter or the subdimension.

    Returns
    -------
    d : dataframe
         with label, code, aggregate type.
    **kwargs:
        https_proxy, deprecated

    """
    assert set(kwargs.keys()).issubset({'https_proxy',}), "Wrong argument."
    __depr__(**kwargs)

    url = __BASE_URL__ + 'codes/' + par + '/' + code
    response = __getresp__(url)
    data = response.json()['data']
    d = []
    for el in data:
        d.append((el['label'], el['code'], el['aggregate_type']))
    d = DataFrame(d, columns=['label','code','aggregate_type'])
    return d


def get_data(code, **kwargs):
    """
    Given the code of a Faostat dataset,
    returns the data as a list of tuples.
    To download only a subset of the dataset, you need to pass pars={key: value, ...}:
    from the codes obtained with get_par_list and get_par.

    Parameters
    ----------
    code : str
        code of the dataset.
    pars : dict, optional
        parameters to retrieve a subset of the dataset:
            {key: value, ...}.
        The default is {}.
    coding : dict, optional
        coding_system of the parameters:
            {key: value, ...}.
        The default is {}.
    show_flags : bool, optional
        True to download also the data flags.
        The default is False.
    null_values : bool, optional
        True to download also the null values.
        The default is False.
    show_notes : bool, optional
        True to download also the notes.
        The default is False.
    strval : bool, optional
        True to keep the values as provided by Faostat (as str),
        False to try to convert them to numbers.
        The default is True.
    https_proxy: deprecated

    Returns
    -------
    l : list
        data with header.

    """
    assert set(kwargs.keys()).issubset({'pars', 'coding', 'show_flags', 'null_values', 
                 'show_notes', 'strval', 'https_proxy'}), "Error: unexpected kwarg."

    __depr__(**kwargs)

    pars = kwargs.get('pars', {})
    coding = kwargs.get('coding', {})
    show_flags = kwargs.get('show_flags', False)
    null_values = kwargs.get('null_values', False)
    show_notes = kwargs.get('show_notes', False)
    strval = kwargs.get('strval', True)
    url = __BASE_URL__ + 'data/' + code
    params = list(pars.items())
    # print('s',params)
    for codsys in coding:
        params += [(codsys + '_cs', coding[codsys]),]
    params += [('show_codes', True),
               ('show_unit', True),
               ('show_flags', show_flags),
               ('show_notes', show_notes),
               ('null_values', null_values),
               ('limit', -1),
               ('output_type', 'objects')    ## ok, da non modificare
               ## datasource sempre production: ok, verificato nei pars
              ]
    # print(params)
    response = __getresp__(url, params=params)
    try:
        dsd = response.json()['metadata']['dsd']
    except:
        print('Warning: seems like no data are available for your selection.')
        return []
    header = tuple([d['label'] for d in dsd])
    l = [header,]
    data = response.json()['data']
    if strval:
        for row in data:
            l += [tuple([row.get(h, None) for h in header]),]
    else:
        for row in data:
            r = []
            for h in header:
                if h != 'Value' and 'Code' not in h:
                    r.append(row.get(h, None))
                else:
                    try:
                        r.append(eval(row.get(h, None)))
                    except:
                        r.append(row.get(h, None))
            l.append(tuple(r))
    return l


def get_data_df(code, **kwargs):
    """
    Given the code of a Faostat dataset,
    returns the data as pandas dataframe.
    To download only a subset of the dataset, you need to pass pars={key: value, ...}:
    from the codes obtained with get_par_list and get_par.
     
    Parameters
    ----------
    code : str
        code of the dataset.
    pars : dict, optional
        parameters to retrieve a subset of the dataset:
            {key: value, ...}.
        The default is {}.
    coding : dict, optional
        coding_system of the parameters:
            {key: value, ...}.
        The default is {}.
    show_flags : bool, optional
        True to download also the data flags.
        The default is False.
    null_values : bool, optional
        True to download also the null values.
        The default is False.
    show_notes : bool, optional
        True to download also the notes.
        The default is False.
    strval : bool, optional
        True to keep the values as provided by Faostat (as str),
        False to try to convert them to numbers.
        The default is True.
    https_proxy: deprecated
     
    Returns
    -------
    l : dataframe
        data with header.
     
    """
    d = get_data(code, **kwargs)
    return DataFrame(d[1:], columns=d[0])


########## DEPRECATED #############

def get_areas(code, **kwargs):
    """
    DEPRECATED - use get_par instead
    Given the code of a Faostat dataset,
    returns the available areas as dict.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    return get_par(code, 'areas', **kwargs)


def get_years(code, **kwargs):
    """
    DEPRECATED - use get_par instead
    Given the code of a Faostat dataset,
    returns the available years as dict.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    return get_par(code, 'years', **kwargs)


def get_elements(code, **kwargs):
    """
    DEPRECATED - use get_par instead
    Given the code of a Faostat dataset,
    returns the available elements as dict.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    return get_par(code, 'elements', **kwargs)


def get_items(code, **kwargs):
    """
    DEPRECATED - use get_par instead
    Given the code of a Faostat dataset,
    returns the available items as dict.

    Parameters
    ----------
    code : str
        code of the dataset.
    https_proxy : list, optional
        parameters for https proxy: 
        [username, password, url:port].
        The default is None (no proxy).

    Returns
    -------
    d : dict
        {label: code, ...}.

    """
    return get_par(code, 'items', **kwargs)


def __depr__(**kwargs):
    if 'https_proxy' in set(kwargs.keys()):
        https_proxy = kwargs['https_proxy']
        if https_proxy == None:
            return
        elif ':' not in https_proxy[2]:
            print("Error in proxy host. It must be in the form: 'url:port'")
            raise
        proxydic = {'https': 'https://' +\
                    https_proxy[0] + ':' +\
                    requests.compat.quote(https_proxy[1]) + '@' +\
                    https_proxy[2]}
        set_requests_args(proxies=proxydic)
        kwargs.pop('https_proxy', None)
    return
