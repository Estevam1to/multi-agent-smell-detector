# GitHub token grabber from private key
# ported from ruby thanks partially to copilot

import jwt
from bpm.config import global_config, update_config
import datetime
import requests

def get_github_token():
    # Get github private key from config
    keyfile = global_config.get("github_private_key", None)
    if not keyfile:
        raise Exception("No github private key found")
    with open(keyfile, "r") as f:
        # get the private keys as string
        private_key = f.read()
        #print(private_key)

    payload = {
            #datetime now - 60 seconds
        "iat": datetime.datetime.utcnow() - datetime.timedelta(seconds=60),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        "iss": "206650" # TODO: get this from config
    }
    jwt_token = jwt.encode(payload, private_key, algorithm="RS256")
    #print(jwt_token)
    # Make a post request to the github api
    # Accept: application/vnd.github.v3+json
    req = requests.post(
        "https://api.github.com/app/installations/26150114/access_tokens",headers={
        "Authorization": "Bearer " + jwt_token,
        "Accept": "application/vnd.github.v3+json"
    })
    #print(req.json())
    old_config = global_config

    old_config["git_token"] = req.json()["token"]
    update_config(old_config)
    return req.json()["token"]

if __name__ == "__main__":
    get_github_token()