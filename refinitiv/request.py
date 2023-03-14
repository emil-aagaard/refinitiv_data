'''
A module to execute requests to Refinitiv.
'''

from . import config
from . import api
from values import Value

# suffixes of parameter strings
formattable_period_str = config['formattable_period_str']
name_str = config['name_str']
date_str = config['date_str']
unit_strs = config['unit_strs']


class Request:
    '''
    A class that sends a request via the `api` module. The 
    data to be fetched is given by `attributes`.

    ...

    Attributes
    ----------
    attributes : dict
        subset of the company attributes `backend/config.json` 
        to be requested
    years : list
        list of consecutive fiscal years to be fetched
    df : pandas.DataFrame
        response from the api
    response : dict
        response in the correct syntax

    Methods
    -------
    build_response():
        builds the response `dict`
    is_mostly_none():
        checks whether the response is mostly empty
    build_parameters(attributes, period_str):
        (static method) builds the request parameters
    get_value_list(values, units, dates, years):
        (static method) produces a `value_list`
    get_value_map(segment_names, values, units, dates, years):
        (static method) produces a `value_map`
    
    '''

    def __init__(self, identifier: str, attributes: dict, years: list):
        '''
        Parameters
        ----------
        identifier : str
            identifier of the company
        attributes : dict
            subset of the company attributes `backend/config.json` 
            to be requested
        years : list
            list of consecutive fiscal years to be fetched
        '''

        self.attributes = attributes
        self.years = years
        period_str = formattable_period_str.format(years[0], years[-1])
        parameters = self.build_parameters(attributes, period_str)        
        self.df = api.get_data(identifier, parameters)
        
        if self.df is None:
            self.response = None

        else:
            self.response = self.build_response()

    def __eq__(self, request):
        return self.__dict__ == request.__dict__

    def build_response(self):
        '''
        Builds the repsonse dictionary from 
        the dataframe `self.df`.

        Returns
        -------
        response : dict
            `dict` containing the fetched values
        '''

        n = 1
        response = {}

        for attribute_key, attribute in self.attributes.items():
            if attribute['type'] == 'other':
                response[attribute_key] = self.df.values[0][n]
                n += 1

            elif attribute['type'] == 'value':
                response[attribute_key] = Value(self.df.values[0][n], self.df.values[0][n+1])
                n += 2
            
            elif attribute['type'] == 'value_list':
                response[attribute_key] = self.get_value_list(*self.df.values[:,n:n+3].T, self.years)
                n += 3

            elif attribute['type'] == 'value_map':
                response[attribute_key] = self.get_value_map(*self.df.values[:,n:n+4].T, self.years)
                n += 4

        return response

    def is_mostly_none(self):
        '''
        Checks if all `value_list`s only contains `Value(None)`.

        Returns
        -------
        bool
        '''

        lists = 0
        none_lists = 0

        for attribute_key, attribute in self.attributes.items():
            if attribute_key in self.response and attribute['type'] == 'value_list':
                none_lists += all([value.value is None for value in self.response[attribute_key]])
                lists += 1

        if lists == none_lists:
            return True
        
        else:
            return False

    @staticmethod
    def build_parameters(attributes, period_str):
        '''
        Builds the request parameters from the 
        `attributes` and the parameter suffixes

        Parameters
        ----------
        attributes : dict
            subset of the company attributes `backend/config.json` 
            to be requested
        period_str : str
            `str` of the appropriate suffix to fetch 
            data from a time range
        
        Returns
        -------
        parameters : list
            parameters for the request
        '''

        parameters = []
        
        for attribute in attributes.values():
            if attribute['type'] == 'other':
                parameters += [attribute['parameter']]

            elif attribute['type'] == 'value':
                parameters += [
                    attribute['parameter'],
                    attribute['parameter']+unit_strs[attribute['unit_type']]
                ]
            
            elif attribute['type'] == 'value_list':
                parameters += [
                    attribute['parameter']+period_str,
                    attribute['parameter']+period_str+unit_strs[attribute['unit_type']],
                    attribute['parameter']+period_str+date_str
                ]

            elif attribute['type'] == 'value_map':
                parameters += [
                    attribute['parameter']+period_str+name_str,
                    attribute['parameter']+period_str,
                    attribute['parameter']+period_str+unit_strs[attribute['unit_type']],
                    attribute['parameter']+period_str+date_str
                ]
        
        return parameters
    
    @staticmethod
    def get_value_list(values, units, dates, years):
        '''
        Converts the inputs into a single `value_list`. We should 
        have the following:
        >>> len(values) == len(units) == len(dates)

        Parameters
        ----------
        values : list
            `list` of response values
        units : list
            `list` of response units
        dates : list
            `list` of response dates
        years : list
            list of consecutive fiscal years
        '''

        output_dict = {year: Value(None) for year in years}
        
        for value, unit, date in zip(values, units, dates):
            if type(date) == str and len(date) >= 4:
                year = int(date[:4])
                output_dict[year] = Value(value, unit)
        
        return list(output_dict.values())

    @staticmethod
    def get_value_map(segment_names, values, units, dates, years):
        '''
        Converts the inputs into a single `value_map`. We should 
        have the following:
        >>> len(segment_names) == len(values) == len(units) == len(dates)

        Parameters
        ----------
        segment_names : list
            `list` of response segment names
        values : list
            `list` of response values
        units : list
            `list` of response units
        dates : list
            `list` of response dates
        years : list
            list of consecutive fiscal years
        '''
        
        output_dict = {year: [] for year in years}
        
        for segment_name, value, unit, date in zip(segment_names, values, units, dates):
            if type(date) == str and len(date) >= 4:
                year = int(date[:4])
                output_dict[year] += [(segment_name, Value(value, unit))]

        return list(output_dict.values())