from . import config
from values import Value, ValueList

def analize_value_lists(companies, analysis_attributes=config['analysis_attributes']):
    results = ValueList([Value(0)]*len(analysis_attributes))

    for company in companies:
        results += check_value_lists(company, analysis_attributes=analysis_attributes)

    results /= ValueList([Value(len(companies))]*len(analysis_attributes))
    results *= Value(100, '%')
    analysis = {analysis_attribute: result for analysis_attribute, result in zip(analysis_attributes, results)}

    return analysis


def check_value_lists(company, analysis_attributes=config['analysis_attributes']):
    result = ValueList()

    for analysis_attribute in analysis_attributes:
        result.append(is_not_only_none(company.__dict__[analysis_attribute]))

    return result


def is_not_only_none(value_list):
    nones = [value for value in value_list if value.value is None]

    return Value(int(len(value_list) != len(nones)))