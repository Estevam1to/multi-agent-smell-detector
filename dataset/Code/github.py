import urllib.request, json

# get all repos from a github user
def get_repos(username):
    url = "https://api.github.com/users/" + username + "/repos"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())
    return data

print(get_repos("joseywoermann"))



# get the names of all repos from a github user
def get_repo_names(username):
    repos = get_repos(username)
    names = []
    for repo in repos:
        names.append(repo["name"])
    return names

print(get_repo_names("joseywoermann"))
