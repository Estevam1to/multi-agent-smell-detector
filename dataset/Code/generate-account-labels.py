'''
Rather than using this hack we should 
be generating a JSON file in the govdirectory website directory 
using Snowman
'''
import argparse
from os import listdir
import json
from hashlib import sha256

snowman_cache_location = '.snowman/cache/'
govdirectory_generators = 'queries/generators/'

supported_platforms = ['twitter', 'facebook', 'github', 'instagram', 'linkedin', 'youtube']

# parse location argument into a file path and return a list of files
parser = argparse.ArgumentParser(description='Generate data from JSON files.')
parser.add_argument('-l', '--location', type=str, help='location of the Govdriectory website project')
args = parser.parse_args()

def resolve_country(country_query):
    country_cache_hash = sha256(('generators/' + country_query).encode('utf-8')).hexdigest()
    country_dir = args.location + snowman_cache_location + country_cache_hash
    print(country_dir)
    country_cache_file = listdir(country_dir)[0]
    print(country_cache_file)
    country_cache_file_full_path = country_dir + '/' + country_cache_file

    country = country_query.replace('.rq', '')

    return (country, country_cache_file_full_path)



# snowman caches files by the following logic: sha256(filepath) / sha256(filecontents)
# we can skip the last part and just pick the first file in the directory as country queries isn't paramiterized
govdirectory_generators_cache = listdir(args.location + govdirectory_generators)
print(govdirectory_generators_cache)
countries = list(map(resolve_country, govdirectory_generators_cache))

print(countries)

orgs = list()

for country in countries:
    with open(country[1], 'r') as f:
        data = json.load(f)
        print(data)
        for org in data['results']['bindings']:
            print(country[0] + '/' + org['qid']['value'])
            orgs.append((country[0], org['qid']['value']))

with open(args.location + 'queries/account-data.rq', 'r') as f:
    account_data_query = f.read()

account_data_file_hash = sha256('account-data.rq'.encode('utf-8')).hexdigest()


final_account_index = list()

for org in orgs:
    query_hash = sha256((account_data_query.replace('''{{.}}''', org[1])).encode('utf-8')).hexdigest()
    account_file_path = args.location + snowman_cache_location + account_data_file_hash + '/' + query_hash + '.json'

    with open(account_file_path, 'r') as f:
        data = json.load(f)
        for account in data['results']['bindings']:
            platform = account['platformLabel']['value'].lower()

            if platform in supported_platforms:
                final_account_index.append((platform, org[0] + '/' + org[1], account['account']['value']))

# very inefficient, I blame CoPilot
facebook = filter(lambda x: x[0] == 'facebook', final_account_index)
twitter = filter(lambda x: x[0] == 'twitter', final_account_index)
github = filter(lambda x: x[0] == 'github', final_account_index)
instagram = filter(lambda x: x[0] == 'instagram', final_account_index)
linkedin = filter(lambda x: x[0] == 'linkedin', final_account_index)
youtube = filter(lambda x: x[0] == 'youtube', final_account_index)

# please do not judge me
json_index = dict()
json_index['facebook'] = dict()
json_index['twitter'] = dict()
json_index['github'] = dict()
json_index['linkedin'] = dict()
json_index['youtube'] = dict()
json_index['instagram'] = dict()


for item in facebook:
    json_index['facebook'][item[2].lower()] = item[1]
for item in twitter:
    json_index['twitter'][item[2].lower()] = item[1]
for item in github:
    json_index['github'][item[2].lower()] = item[1]
for item in linkedin:
    json_index['linkedin'][item[2].lower()] = item[1]
for item in youtube:
    json_index['youtube'][item[2].lower()] = item[1]
for item in instagram:
    json_index['instagram'][item[2].lower()] = item[1]

print(json_index)

js = 'const accountIndex = ' + json.dumps(json_index) + ';'

open('scripts/account_index.js', 'w').write(js)
