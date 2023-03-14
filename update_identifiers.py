from refinitiv import api
import json

search_string = 'TR.HQCountryCode=DK, TR.HasESGCoverage=False'
df = api.get_data('SCREEN(U(IN(Equity(active,public,private,primary))), {})'.format(search_string), ['TR.OrganizationID'])
identifiers = list(df.values[:,1])

with open('data/identifiers.json', 'w') as file:
    json.dump(identifiers, file)