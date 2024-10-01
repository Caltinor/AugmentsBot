import requests
import json

try:
    tokenFile = open("ghtoken.txt", 'r')
    token = tokenFile.readline()
    tokenFile.close()

    headers = {"Authorization" : f"Bearer {token}",
        "Accept": "application/vnd.github+json"}
except FileNotFoundError:
    print("ghtoken.txt not found!")

def createIssue(Repositoryname : str, title :str, body :str):
    data = {"title": title, "body": body}
    url = f"https://api.github.com/repos/Caltinor/{Repositoryname}/issues"
    requests.post(url,data=json.dumps(data),headers=headers)
