from company.company import Company
from coverage.analysis import get_analysis, save_analysis
import json
from tqdm import tqdm
from numpy.random import shuffle
import time


def get_identifiers():
    with open('data/identifiers.json') as file:
        identifiers = json.load(file)

    return identifiers


def get_companies(identifiers, first_index=None, last_index=None, randomize=False, error_sleep=10, max_n_errors=5):
    companies = {}

    if randomize:
        shuffle(identifiers)

    for identifier in tqdm(identifiers[first_index:last_index]):
        if identifier is not None:
            n_errors = 0

            while n_errors < max_n_errors:
                try:
                    company = Company(identifier)
                    companies[identifier] = company
                    break
                
                except:
                    print(f'Error occured at identifier {identifier}.')
                    n_errors += 1
                    time.sleep(error_sleep)

            if n_errors == max_n_errors:
                print(f'Too many errors occured at identifier {identifier}. It will be skipped.')

    return companies


def save_companies(companies):
    company_dicts = {identifier: company.to_dict() for identifier, company in companies.items()}

    with open('data/companies.json', 'w') as file:
        json.dump(company_dicts, file)


if __name__ == '__main__':
    identifiers = get_identifiers()
    companies = get_companies(identifiers)
    save_companies(companies)
    analysis = get_analysis(companies.values())
    save_analysis(analysis)
