from company.company import Company
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
            companies[identifier] = company.to_dict()

    return companies


def save_companies(companies):
    with open('data/companies.json', 'w') as file:
        json.dump(companies, file)



if __name__ == '__main__':
    identifiers = get_identifiers()
    companies = get_companies(identifiers)
    save_companies(companies)