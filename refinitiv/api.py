'''
This module, when imported, initializes an Eikon app, 
which enables us to fetch data from the Eikon data api 
proxy.

The following are names of the parameters that represent 
geographical revenue:

>>> fields=['TR.F.GEOSegRevPct.segmentName', 'TR.F.GEOSegRevPct']
>>> fields=['TR.BGS.GeoTotalRevenue.segmentName', 'TR.BGS.GeoTotalRevenue']
>>> fields=['TR.F.BUSEXTREVASR.segmentName', 'TR.F.BUSEXTREVASR']
>>> fields=['TR.F.BUSExtRev.segmentName', 'TR.F.BUSExtRev']
>>> fields=['TR.F.GEOExtRev.segmentName', 'TR.F.GEOExtRev']
'''

import eikon
from time import sleep
from numpy import nan

eikon.set_app_key('942784cb18244d7f84c1947c990b63ab5fa491bc')

def get_data(identifier, parameters):
    '''
    Fetches data from the Eikon data api. 
    It sleeps in 0.3 seconds to avoid 
    overloading the api.

    Parameters
    ----------
    identifier : str
        identifier of the company that can be 
        recognized by the Eikon data api e.g. ISIN
    parameters : list
        Refinitiv parameters for the request

    Returns
    -------
    pandas.DataFrame or None
        the response the api
    '''
    
    sleep(0.3)

    df, _ = eikon.get_data(identifier, parameters)
    
    if df is None:
        return None

    else:
        return df.fillna(nan).replace([nan], [None])

if __name__ == '__main__':
    df = get_data('AAPL.O', ['TR.MilitaryWeaponsorPersonnel'])