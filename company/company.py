from . import company_attributes
from values import Value, get_unit
import refinitiv.request
from datetime import datetime

current_year = datetime.now().year


class Company:
    '''
    A class that represents a company. Once an object 
    is initialized, it fetches all data of the company 
    matching the `identifier` (RIC, ISIN, ticker, ...).

    ...

    Attributes
    ----------
    All attributes are listed in `backend/config.json` 
    under `"company_attributes"`. There are four different 
    types of attributes:

    other : Any
        any variable that should be passed on to the 
        frontend without any formatting (must be 
        JSON serializable)
    value : Value
        an instance of the `Value` class
    value_list : list
        list of lists of `Value` objects
    value_map : list
        list of lists of `[GeoPlace, Value]`-type lists
    
    Each element in a `value_list` or `value_map` corresponds 
    to a year:
    >>> len(value_list) == len(value_map) == len(self.years)

    Methods
    -------
    set_empty_attributes(years):
        sets all attributes to an initial state (of `None`s)
    set_attributes(self, attributes_dict):
        sets the attributes as dictated by `attributes_dict`
    to_dict():
        converts the object into a JSON serializable `dict`
    '''
    
    def __init__(self, identifier: str, years_back: int=10):
        '''
        Gathers all data on company.

        Parameters
        ----------
        identifier : str
            identifier of the company that can be 
            recognized by the Eikon data api e.g. ISIN
        years_back : int
            number of consecutive fiscal years to 
            be analyzed

        Returns
        -------
        None
        '''

        years = list(range(current_year, current_year-years_back-1, -1))
        self.set_empty_attributes(years)
        self.years = years

        refinitiv_request_attributes = get_source_attributes(company_attributes, 'refinitiv')
        refinitiv_request = refinitiv.request.Request(identifier, refinitiv_request_attributes, self.years)

        # sends a new refinitiv request with the RIC if not much data was found
        if (refinitiv_request.response is not None and
                refinitiv_request.is_mostly_none() and
                refinitiv_request.response['ric'] is not None):
            refinitiv_request = refinitiv.request.Request(refinitiv_request.response['ric'], refinitiv_request_attributes, self.years)

        if refinitiv_request.response is None:
            self.error = True
            self.name = identifier

        else:
            self.error = False
            self.set_attributes(refinitiv_request.response)
            
    def __eq__(self, company):
        return self.__dict__ == company.__dict__
            
    def set_empty_attributes(self, years):
        '''
        Sets all attributes equal to a None- or 
        empty version of their type, abd ensures 
        that the `value_list`s and `value_maps` 
        have the correct lengths (`== len(self.years)`)

        Parameters
        ----------
        years : list
            list of consecutive fiscal years
        
        Returns
        -------
        None
        '''

        for attribute_key, attribute in company_attributes.items():
            if attribute['type'] == 'other':
                self.__dict__[attribute_key] = None

            elif attribute['type'] == 'value':
                self.__dict__[attribute_key] = Value(None)
            
            elif attribute['type'] == 'value_list':
                self.__dict__[attribute_key] = [Value(None) for _ in years]

            elif attribute['type'] == 'value_map':
                self.__dict__[attribute_key] = [[] for _ in years]

    def set_attributes(self, attributes_dict):
        '''
        Sets the attributes dictated by the keys 
        `attributes_dict` equal to the values of 
        the corresponding values of `attributes_dict`.

        Parameters
        ----------
        attributes_dict : dict
            `dict` to dictate the attributes

        Returns
        -------
        None
        '''

        for attribute_key, attribute in attributes_dict.items():
            self.__dict__[attribute_key] = attribute

    def to_dict(self):
        '''
        Outputs a `dict` that represents the company in 
        the format that is required for `companies.json`. 
        If an attribute's name begin with `_temp` it will 
        be skipped.

        Returns
        -------
        dict_ : dict
            `dict` of the attributes of the object
        '''

        dict_ = {}

        for attribute_key in company_attributes:
            if attribute_key.startswith('temp_'):
                continue

            attribute = self.__getattribute__(attribute_key)
            type_ = company_attributes[attribute_key]['type']
            dict_[attribute_key] = {}
            dict_[attribute_key]['name'] = company_attributes[attribute_key]['name']

            if type_ == 'other':
                dict_[attribute_key]['value'] = attribute
                dict_[attribute_key]['unit'] = None

            elif type_ == 'value':
                dict_[attribute_key]['value'] = attribute.value
                dict_[attribute_key]['unit'] = attribute.unit
            
            elif type_ == 'value_list':
                unit = get_unit(attribute)
                dict_[attribute_key]['value'] = [value.value for value in attribute]
                dict_[attribute_key]['unit'] = unit
            
            elif type_ == 'value_map':
                values = [tuple_[1] for tuple_ in sum(attribute, [])]
                unit = get_unit(values)
                dict_[attribute_key]['value'] = [[[tuple_[0].name, tuple_[1].value] for tuple_ in tuples] for tuples in attribute]
                dict_[attribute_key]['unit'] = unit
            
        return dict_
    

def get_source_attributes(company_attributes, source):
    '''
    Outputs all attributes with the given source.

    Parameters
    ----------
    company_attributes : dict
        all company attributes from `backend/config.json`
    source : str
        a source

    Returns
    -------
    request_attributes : dict
        subset of `company_attributes`
    '''

    request_attributes = {attribute_key: attribute_value for \
        attribute_key, attribute_value in company_attributes.items() if attribute_value['source'] == source}

    return request_attributes