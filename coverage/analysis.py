from . import config
from company import company_attributes
from values import Value, ValueList
import json

def get_analysis(companies, analysis_attributes=config['analysis_attributes'], company_attributes=company_attributes):
    results = ValueList([Value(0)]*len(analysis_attributes))

    for company in companies:
        results += analize_company(company, analysis_attributes=analysis_attributes, company_attributes=company_attributes)

    results /= ValueList([Value(len(companies))]*len(analysis_attributes))
    results *= Value(100, '%')
    analysis = {analysis_attribute: result for analysis_attribute, result in zip(analysis_attributes, results)}

    return analysis


def analize_company(company, analysis_attributes=config['analysis_attributes'], company_attributes=company_attributes):
    result = ValueList()

    for analysis_attribute in analysis_attributes:
        if company_attributes[analysis_attribute]['type'] == 'other':
            result.append(Value(int(company.__dict__[analysis_attribute] is not None)))

        elif company_attributes[analysis_attribute]['type'] == 'value_list':
            result.append(is_not_only_none(company.__dict__[analysis_attribute]))

    return result


def is_not_only_none(value_list):
    nones = [value for value in value_list if value.value is None]

    return Value(int(len(value_list) != len(nones)))


def save_analysis(analysis, path=config['analysis_path']):
    analysis_dict = {analysis_attribute: value.value for analysis_attribute, value in analysis.items()}

    with open(path, 'w') as file:
        json.dump(analysis_dict, file)