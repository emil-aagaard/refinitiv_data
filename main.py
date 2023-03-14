from company.company import Company
from coverage.analysis import analize_value_lists
import json
from tqdm import tqdm
from numpy.random import shuffle


def get_identifiers():
    with open('data/identifiers.json') as file:
        identifiers = json.load(file)

    return identifiers


def get_companies(identifiers, first_index=None, last_index=None, randomize=False):
    companies = {}

    if randomize:
        shuffle(identifiers)

    for identifier in tqdm(identifiers[first_index:last_index]):
        if identifier is not None:
            company = Company(identifier)
            companies[identifier] = company

    return companies


def save_companies(companies):
    company_dicts = {identifier: company.to_dict() for identifier, company in companies.items()}

    with open('data/companies.json', 'w') as file:
        json.dump(company_dicts, file)


if __name__ == '__main__':
    identifiers = get_identifiers()
    companies = get_companies(identifiers)
    save_companies(companies)
    analysis = analize_value_lists(companies.values())
